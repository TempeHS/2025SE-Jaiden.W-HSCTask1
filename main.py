from flask import Flask, render_template, request, redirect, flash, session, send_file
from flask_wtf.csrf import CSRFProtect
from flask_csp.csp import csp_header
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flask_session import Session
import logging
import io
import json
from forms import LoginForm, SignUpForm, TwoFactorForm, LogEntryForm, DeleteUserForm
from datetime import timedelta
from formHandlers import handle_login, handle_two_factor, handle_log_entry, handle_sign_up, handle_entries
from databaseManagement import retrieveUserData, deleteUserData
from profileHandler import downloadData, deleteData

app = Flask(__name__)
app.secret_key = b"hSWrqNxeExuR03aq;apl"
csrf = CSRFProtect(app)
limiter = Limiter(get_remote_address, app=app)
cors = CORS(app) 
app.config["CORS_HEADERS"] = "Content-Type"

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
    if request.method == 'GET':
        if 'username' not in session:
            return redirect("/login.html")
        username = session['username']
        logEntryForm = LogEntryForm(username=username)
        return render_template('index.html', form=logEntryForm)
    return handle_log_entry(logEntryForm)

@app.route("/login.html", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    loginForm = LoginForm()
    return handle_login(loginForm)

@app.route("/2fa", methods=["GET", "POST"])
def two_factor():
    twoFactorForm = TwoFactorForm()
    return handle_two_factor(twoFactorForm)

@app.route("/signUp.html", methods=["GET", "POST"])
def sign_up():
    signUpForm = SignUpForm()
    return handle_sign_up(signUpForm)

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html") 

@app.route('/entries.html', methods=['GET'])
def entries():
    return handle_entries()

@app.route("/profile.html", methods=["GET"])
def profile():
    if 'username' not in session:
        return redirect("/login.html")
    username = session['username']
    deleteUserForm = DeleteUserForm()
    return render_template("/profile.html", username=username, form=deleteUserForm)

@app.route("/download_data", methods=["GET"])
def download_data():
    return downloadData(app)

@app.route("/delete_data", methods=["POST"])
def delete_data():
    return deleteData(app)

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
