from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from userLogic import login_user, signup_user  

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

if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)