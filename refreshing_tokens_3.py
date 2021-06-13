# Token Freshness Pattern

from datetime import timedelta

from flask import Flask, jsonify, request

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "soosoo"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=5)
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
  username = request.json.get("username", None)
  password = request.json.get("password", None)
  if username != "soosoo" or password != "1234":
    return jsonify({"msg": "Bad username pr password"}), 401
  
  access_token = create_access_token(identity=username, fresh=True)
  refresh_token = create_refresh_token(identity=username)
  return jsonify(access_token=access_token, refresh_token=refresh_token)


@app.route("/refresh", methods={"POST"})
@jwt_required(refresh=True)
def refresh():
  identity = get_jwt_identity()
  access_token = create_access_token(identity=identity, fresh=False)
  return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
  return jsonify(foo="bar")


@app.route("/protected_fresh", methods=["GET"])
@jwt_required(fresh=True)
def protected_fresh():
  return jsonify(foo="bar_fresh")


if __name__ == "__main__":
  app.run()