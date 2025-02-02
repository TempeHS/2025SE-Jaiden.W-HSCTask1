from flask import flash, session, redirect, render_template, request, url_for
import requests
import logging
import databaseManagement as dbHandler
from twoFactor import generate_totp_secret, get_totp_uri, generate_qr_code, verify_totp
from sanitize import sanitize_data, sanitize_input
from timestampRounding import get_rounded_timestamp

app_log = logging.getLogger(__name__)
app_header = {"Authorisation": "uPTPeF9BDNiqAkNj"}

def handle_login(loginForm):
    rate_limit_exceeded = False 
    if loginForm.validate_on_submit():
        sanitized_data = sanitize_data({
            "username": loginForm.username.data,
            "password": loginForm.password.data
        })
        try:
            response = requests.post("http://127.0.0.1:3000/api/login", json=sanitized_data, headers=app_header)
            response.raise_for_status()
            if response.status_code == 200:
                session['username'] = loginForm.username.data
                session.permanent = True  # Mark the session as permanent
                app_log.info("User '%s' logged in, hasn't passed 2FA", loginForm.username.data)
                return redirect(url_for('two_factor'))
            else:
                flash('Invalid username or password', 'danger')
                app_log.warning("Failed login attempt for user: %s", loginForm.username.data)
        except requests.exceptions.HTTPError as e:
            flash('Invalid username or password', 'danger')
            app_log.error("Invalid login attempt for user: %s - %s", loginForm.username.data, str(e))
        except requests.exceptions.RequestException as e:
            flash('An error occurred. Please try again later.', 'danger')
            app_log.error("Error during login attempt for user: %s - %s", loginForm.username.data, str(e))
    return render_template("login.html", form=loginForm, rate_limit_exceeded=rate_limit_exceeded)

def handle_two_factor(twoFactorForm):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user = dbHandler.retrieveUserByUsername(username)
    if not user:
        return redirect(url_for('login'))
    secret = user.get('totp_secret')
    if not secret: #exception handling for users without 2FA secret
        secret = generate_totp_secret()
        dbHandler.updateUserTotpSecret(username, secret)
    uri = get_totp_uri(secret, username)
    qr_code = generate_qr_code(uri)
    if request.method == "POST" and twoFactorForm.validate_on_submit():
        token = twoFactorForm.token.data
        if verify_totp(token, secret):
            app_log.info("2FA successful, User '%s' logged in successfully", username)
            return redirect(url_for('root'))
        else:
            flash('Invalid 2FA token', 'danger')
            app_log.warning("Invalid 2FA token for user: %s", username)
    return render_template("2fa.html", form=twoFactorForm, qr_code=qr_code)

def handle_log_entry(logEntryForm):
    if request.method == 'POST':
        logEntryForm.sanitizeLogData()
        data = {
            "developer": logEntryForm.developer.data,
            "project": logEntryForm.project.data,
            "start_time": logEntryForm.start_time.data.strftime('%Y-%m-%d %H:%M'),
            "end_time": logEntryForm.end_time.data.strftime('%Y-%m-%d %H:%M'),
            "time_worked": float(logEntryForm.time_worked.data),  # Convert Decimal to float
            "repo": logEntryForm.repo.data,
            "developer_notes": logEntryForm.developer_notes.data,
            "developer_code": logEntryForm.developer_code.data,
            "diary_entry": get_rounded_timestamp()  # Add rounded timestamp
        }
        try:
            response = requests.post("http://127.0.0.1:3000/api/logEntry", json=data, headers=app_header)
            response.raise_for_status()
            if response.status_code == 201:
                flash('Log entry submitted successfully.', 'success')
                app_log.info("Log entry submitted successfully by developer: %s", logEntryForm.developer.data)
            else:
                flash('An error occurred during log entry submission. Please try again.', 'danger')
                app_log.warning("Failed log entry submission by developer: %s", logEntryForm.developer.data)
        except requests.exceptions.RequestException as e:
            flash('An error occurred. Please try again later.', 'danger')
            app_log.error("Error during log entry submission by developer: %s - %s", logEntryForm.developer.data, str(e))
        return render_template('index.html', form=logEntryForm)
    
def handle_sign_up(signUpForm):
    if signUpForm.validate_on_submit():
        sanitized_data = sanitize_data({
            "username": signUpForm.username.data,
            "password": signUpForm.password.data
        })        
        try:
            response = requests.post("http://127.0.0.1:3000/api/signup", json=sanitized_data, headers=app_header)
            response.raise_for_status()
            if response.status_code == 201:
                app_log.info("User '%s' signed up successfully", signUpForm.username.data)
                flash('Sign up successful. Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('An error occurred during sign up. Please try again.', 'danger')
                app_log.warning("Failed signup attempt for user: %s", signUpForm.username.data)
        except requests.exceptions.RequestException as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            app_log.error("Error during signup attempt for user: %s - %s", signUpForm.username.data, str(e))
    else:
        for field, errors in signUpForm.errors.items():
            for error in errors: 
                flash(f"Error in {getattr(signUpForm, field).label.text}: {error}", 'danger')
                app_log.warning("Validation error in %s: %s", getattr(signUpForm, field).label.text, error)
    return render_template('signUp.html', form=signUpForm)

def handle_entries():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = request.args.get('query')
    category = request.args.get('category')
    query = sanitize_input(query) if query else None
    category = sanitize_input(category) if category else None
    allowed_categories = ["developer", "project", "developer_notes", "developer_code"]  # List of allowed column names
    if category and category not in allowed_categories:
        flash('Invalid category', 'danger')
        return render_template('entries.html', log_entries=[])
    params = {'query': query, 'category': category} if query and category else {}
    try:
        response = requests.get("http://127.0.0.1:3000/api/logEntries", headers=app_header, params=params)
        response.raise_for_status()
        log_entries = response.json()
        app_log.info("Successfully fetched log entries")
        return render_template('entries.html', log_entries=log_entries)
    except requests.exceptions.RequestException as e:
        flash('An error occurred while fetching log entries. Please try again later.', 'danger')
        app_log.error("Error fetching log entries: %s", str(e))
        return render_template('entries.html', log_entries=[])