# Explicit Refreshing With Refresh Tokens

from datetime import timedelta

from flask import Flask, jsonify

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "soosoo"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=5)
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
  access_token = create_access_token(identity="example_user")
  refresh_token = create_refresh_token(identity="example_user")
  return jsonify(access_token=access_token, refresh_token=refresh_token)


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
  identity = get_jwt_identity()
  access_token = create_access_token(identity=identity)
  return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
  return jsonify(foo="bar")


if __name__ == "__main__":
  app.run()