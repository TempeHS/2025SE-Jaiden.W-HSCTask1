from flask import Flask, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from flask_csp.csp import csp_header
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import logging
from forms import LoginForm, SignUpForm
import requests

app = Flask(__name__)
app.secret_key = b"hSWrqNxeExuR03aq;apl"
api_key = "uPTPeF9BDNiqAkNj"
csrf = CSRFProtect(app)
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# Custom error handler for rate limit exceeded
@app.errorhandler(429)
def ratelimit_handler(e):
    flash("Too many incorrect attempts. Please try again later.", "danger")
    form = LoginForm()
    return render_template("index.html", form=form, rate_limit_exceeded=True), 429

# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)  # Redirect to the root URL

# Route for the login page
@app.route("/", methods=["GET"])
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
    }
)
def login():
    form = LoginForm()
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    return render_template("index.html", form=form, rate_limit_exceeded=False)

@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute", key_func=get_remote_address)
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        url = "http://127.0.0.1:3000/api/login"
        data = {
            "username": form.username.data,
            "password": form.password.data
        }
        headers = {
            "Authorisation": api_key
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                app.logger.info(f"Successful login attempt for user: {form.username.data}")
                return redirect("/form.html")
            else:
                app.logger.warning(f"Failed login attempt for user: {form.username.data}")
                flash('Invalid username or password', 'danger')
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error during login attempt for user: {form.username.data} - {str(e)}")
            flash('Incorrect username and/or password', 'danger')
    else:
        app.logger.warning(f"Failed login attempt with invalid form data for user: {form.username.data}")
    return render_template("index.html", form=form, rate_limit_exceeded=False)

# Sign up route
@app.route("/signUp.html", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if form.validate_on_submit():
        url = "http://127.0.0.1:3000/api/signup"
        data = {
            "username": form.username.data,
            "password": form.password.data
        }
        headers = {
            "Authorisation": api_key
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            if response.status_code == 201:
                return redirect("/index.html")
            else:
                flash('An error occurred during sign up. Please try again.', 'danger')
        except requests.exceptions.RequestException as e:
            flash(f'An error occurred: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
    return render_template('signUp.html', form=form)

# Route for the privacy policy page
@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")  # Render the privacy policy page

# Route for log entries
@app.route('/form.html', methods=['GET','POST'])
def log ():
    return render_template('form.html')

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
