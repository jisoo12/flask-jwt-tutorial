# Implicit Refreshing With Cookies

from datetime import datetime, timedelta, timezone
from os import access

from flask import Flask, jsonify

from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies


app = Flask(__name__)

app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = "soosoo"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)

jwt = JWTManager(app)


@app.after_request
def refresh_expiring_jwts(response):
  try:
    exp_timestamp = get_jwt()["exp"]
    now = datetime.now(timezone.utc)
    target_timestamp = datetime.timestamp(now + timedelta(seconds=30))
    if target_timestamp > exp_timestamp:
      access_token = create_access_token(identity=get_jwt_identity())
      set_access_cookies(response, access_token)
    return response
  except (RuntimeError, KeyError):
    return response


@app.route("/login", methods=["POST"])
def login():
  response = jsonify({"msg": "login successful"})
  access_token = create_access_token(identity="example_user")
  set_access_cookies(response, access_token)
  return response


@app.route("/logout", methods=["POST"])
def logout():
  response = jsonify({"msg": "logout successful"})
  unset_jwt_cookies(response)
  return response


@app.route("/protected")
@jwt_required()
def protected():
  return jsonify(foo="bar")


if __name__ == "__main__":
  app.run()