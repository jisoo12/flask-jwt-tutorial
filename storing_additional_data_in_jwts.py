from flask import Flask, jsonify, request

from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "soosoo"
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
  username = request.json.get("username", None)
  password = request.json.get("password", None)
  if username != "soosoo" or password != "1234":
    return jsonify({"msg": "Bad username or password"}), 401

  additional_claims = {"aud": "some_audience", "foo": "bar"}
  access_token = create_access_token(username, additional_claims=additional_claims)
  return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
  claims = get_jwt()
  return jsonify(foo=claims["foo"])


if __name__ == "__main__":
  app.run()