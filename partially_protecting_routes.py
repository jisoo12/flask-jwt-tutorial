from flask import Flask, jsonify, request

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "soosoo"
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
  username = request.json.get("username", None)
  password = request.json.get("password", None)
  if username != "soosoo" or password != "1234":
    return jsonify({"msg": "Bad username or password"}),401
  
  access_token = create_access_token(identity=username)
  return jsonify(access_token=access_token)


@app.route("/optionally_protected", methods=["GET"])
@jwt_required(optional=True)
def optionally_protected():
  current_identity = get_jwt_identity()
  if current_identity:
    return jsonify(logged_in_as=current_identity)
  else:
    return jsonify(logged_in_as="anonymous user")


if __name__ == "__main__":
  app.run()