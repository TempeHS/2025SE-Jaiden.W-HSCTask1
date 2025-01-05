from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateTimeField, DecimalField, URLField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import databaseManagement as dbHandler
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Code snippet for logging a message
# app.logger.critical("message")
app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# Generate a unique basic 16 key: https://acte.ltd/utils/randomkeygen
app = Flask(__name__)
app.secret_key = b"hSWrqNxeExuR03aq;apl"  # Secret key for CSRF protection and session management
csrf = CSRFProtect(app)  # Initialize CSRF protection

# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)  # Redirect to the root URL

# Define the login, sign-up, log-entry form using Flask-WTF
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Username field with validation
    password = PasswordField('Password', validators=[DataRequired()])  # Password field with validation
    submit = SubmitField('Log In')  # Submit button
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  
    password = PasswordField('Password', validators=[DataRequired()])  
    submit = SubmitField('Sign Up')  

# Route for the login page
@app.route("/", methods=["POST", "GET"])
@csp_header(
    {
        # Server Side CSP is consistent with meta CSP in layout.html
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
    if form.validate_on_submit():
        user = dbHandler.retrieveUserByUsername(form.username.data)
        if user and check_password_hash(user['password'], form.password.data):
            return redirect("/form.html")
        else:
            flash('Invalid username or password', 'danger')
    return render_template("index.html", form=form)  # Render the login page with the form

# Route for the sign up page
@app.route('/signUp.html', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()  # Create an instance of the sign up form
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        try:
            hashed_password = generate_password_hash(form.password.data)
            dbHandler.insertUser(form.username.data, hashed_password)
            return redirect("/index.html")
        except Exception as e:
            return render_template("signUp.html", error=True, message=str(e), form=form)
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
