from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from userLogic import login_user, signup_user  
import databaseManagement as dbHandler

api = Flask(__name__)
cors = CORS(api)
api.config["CORS_HEADERS"] = "Content-Type"
auth_key = "uPTPeF9BDNiqAkNj"
limiter = Limiter(
    get_remote_address,
    app=api,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

logging.basicConfig(level=logging.DEBUG)

def check_api_key():
    if request.headers.get("Authorisation") != auth_key:
        return jsonify({"message": "Invalid or missing API key"}), 401

@api.route("/api/login", methods=["POST"])
def api_login():
    auth_response = check_api_key()
    if auth_response:
        return auth_response
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    response, status_code = login_user(username, password)
    return jsonify(response), status_code

@api.route("/api/signup", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def api_signup():
    auth_response = check_api_key()
    if auth_response:
        return auth_response
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    try:
        response, status_code = signup_user(username, password)
        return jsonify(response), status_code
    except Exception as e:
        api.logger.error(f"Error during signup: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@api.route("/api/logEntry", methods=["POST"])
@limiter.limit("10 per minute")
def api_log_entry():
    auth_response = check_api_key()
    if auth_response:
        return auth_response
    data = request.get_json()
    developer = data.get("developer")
    project = data.get("project")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    time_worked = data.get("time_worked")
    repo = data.get("repo")
    developer_notes = data.get("developer_notes")
    developer_code = data.get("developer_code")
    try:
        dbHandler.insertLogEntry(developer, project, start_time, end_time, time_worked, repo, developer_notes, developer_code)
        api.logger.info("Log entry submitted successfully")
        return jsonify({"message": "Log entry submitted successfully"}), 201
    except Exception as e:
        api.logger.error(f"Error during log entry submission: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)