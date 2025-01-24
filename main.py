from flask import Flask, render_template, request, redirect, flash, session, send_from_directory
from flask_wtf.csrf import CSRFProtect
from flask_csp.csp import csp_header
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flask_session import Session
import logging
from forms import LoginForm, SignUpForm, TwoFactorForm, LogEntryForm
import requests
from twoFactor import generate_totp_secret, get_totp_uri, generate_qr_code, verify_totp
from datetime import timedelta
import databaseManagement as dbHandler
from sanitize import sanitize_data

app = Flask(__name__)
app.secret_key = b"hSWrqNxeExuR03aq;apl"
csrf = CSRFProtect(app)
limiter = Limiter(get_remote_address, app=app)
cors = CORS(app) 
app.config["CORS_HEADERS"] = "Content-Type"
app_header = {"Authorisation": "uPTPeF9BDNiqAkNj"}

# Initialize logging
app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
)

# Flask-Session configuration
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True  # Make sessions permanent
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1440)  # Set session lifetime to 24 hrs
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "session:"
app.config["SESSION_FILE_DIR"] = "./.flask_session/"
app.config["SESSION_FILE_THRESHOLD"] = 100
Session(app)

# Custom error handler for rate limit exceeded
@app.errorhandler(429)
def ratelimit_handler(e):
    flash("Too many incorrect attempts. Please try again later.", "danger")
    app_log.warning("Rate limit exceeded for IP: %s", request.remote_addr)
    return render_template("login.html", form=LoginForm(), rate_limit_exceeded=True), 429

# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)  # Redirect to the root URL

@app.route("/", methods=["GET", "POST"])
@csp_header(
    {
        "base-uri": "'self'",
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self'",
        "img-src": "'self' data:",
        "media-src": "'self'",
        "font-src": "'self'",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'",
        "manifest-src": "'self'",
    }
)
def submit_log():
    form = LogEntryForm()
    if request.method == 'GET':
        if 'username' not in session:
            return redirect("/login.html")
        return render_template('index.html', form=form)
    
    if request.method == 'POST':
        form.sanitizeLogData()
        data = {
            "developer": form.developer.data,
            "project": form.project.data,
            "start_time": form.start_time.data.isoformat(),  # Convert datetime to ISO 8601 string
            "end_time": form.end_time.data.isoformat(),  # Convert datetime to ISO 8601 string
            "time_worked": float(form.time_worked.data),  # Convert Decimal to float
            "repo": form.repo.data,
            "developer_notes": form.developer_notes.data,
            "developer_code": form.developer_code.data
        }
        try:
            response = requests.post("http://127.0.0.1:3000/api/logEntry", json=data, headers=app_header)
            response.raise_for_status()
            if response.status_code == 201:
                flash('Log entry submitted successfully.', 'success')
                app_log.info("Log entry submitted successfully by developer: %s", form.developer.data)
            else:
                flash('An error occurred during log entry submission. Please try again.', 'danger')
                app_log.warning("Failed log entry submission by developer: %s", form.developer.data)
        except requests.exceptions.RequestException as e:
            flash('An error occurred. Please try again later.', 'danger')
            app_log.error("Error during log entry submission by developer: %s - %s", form.developer.data, str(e))
        return render_template('index.html', form=form)

@app.route("/login.html", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_data({
            "username": form.username.data,
            "password": form.password.data
        })
        try:
            response = requests.post("http://127.0.0.1:3000/api/login", json=sanitized_data, headers=app_header)
            response.raise_for_status()
            if response.status_code == 200:
                session['username'] = form.username.data
                session.permanent = True  # Mark the session as permanent
                app_log.info("User '%s' logged in, hasn't passed 2FA", form.username.data)
                return redirect("/2fa")
            else:
                flash('Invalid username or password', 'danger')
                app_log.warning("Failed login attempt for user: %s", form.username.data)
        except requests.exceptions.HTTPError as e:
            flash('Invalid username or password', 'danger')
            app_log.error("HTTPError during login attempt for user: %s - %s", form.username.data, str(e))
        except requests.exceptions.RequestException as e:
            flash('An error occurred. Please try again later.', 'danger')
            app_log.error("Error during login attempt for user: %s - %s", form.username.data, str(e))
    return render_template("login.html", form=form, rate_limit_exceeded=False)

@app.route("/2fa", methods=["GET", "POST"])
def two_factor():
    form = TwoFactorForm()
    if 'username' not in session:
        return redirect("/")
    username = session['username']
    user = dbHandler.retrieveUserByUsername(username)
    if not user:
        return redirect("/")
    secret = user.get('totp_secret')
    if not secret: #exception handling for users without 2FA secret
        secret = generate_totp_secret()
        dbHandler.updateUserTotpSecret(username, secret)
    uri = get_totp_uri(secret, username)
    qr_code = generate_qr_code(uri)
    if request.method == "POST" and form.validate_on_submit():
        token = form.token.data
        if verify_totp(token, secret):
            app_log.info("2FA successful, User '%s' logged in successfully", username)
            return redirect("/index.html")
        else:
            flash('Invalid 2FA token', 'danger')
            app_log.warning("Invalid 2FA token for user: %s", username)
    
    return render_template("2fa.html", form=form, qr_code=qr_code)

@app.route("/signUp.html", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_data({
            "username": form.username.data,
            "password": form.password.data
        })        
        try:
            response = requests.post("http://127.0.0.1:3000/api/signup", json=sanitized_data, headers=app_header)
            response.raise_for_status()
            if response.status_code == 201:
                app_log.info("User %s signed up successfully", form.username.data)
                return redirect("/login.html")
            else:
                flash('An error occurred during sign up. Please try again.', 'danger')
                app_log.warning("Failed signup attempt for user: %s", form.username.data)
        except requests.exceptions.RequestException as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            app_log.error("Error during signup attempt for user: %s - %s", form.username.data, str(e))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
                app_log.warning("Validation error in %s: %s", getattr(form, field).label.text, error)
    return render_template('signUp.html', form=form)

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")  # Render the privacy policy page

@app.route('/entries.html', methods=['GET'])
def entries():
    if 'username' not in session:
        return redirect("login.html")
    try:
        response = requests.get("http://127.0.0.1:3000/api/logEntries", headers=app_header)
        response.raise_for_status()
        log_entries = response.json()
        app_log.info("Successfully fetched log entries")
        return render_template('entries.html', log_entries=log_entries)
    except requests.exceptions.RequestException as e:
        flash('An error occurred while fetching log entries. Please try again later.', 'danger')
        app_log.error("Error fetching log entries: %s", str(e))
        return render_template('entries.html', log_entries=[])

@app.route("/logout")
def logout():
    username = session.pop('username', None)
    if username:
        app_log.info("User '%s' logged out successfully", username)
    flash('You have been logged out.', 'success')
    return redirect("login.html")

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
