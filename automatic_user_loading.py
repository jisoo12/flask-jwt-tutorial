from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_str_cmp

from flask_jwt_extended import create_access_token, current_user, jwt_required, JWTManager


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "soosoo"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

jwt = JWTManager(app)
db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text, nullable=False, unique=True)
  full_name = db.Column(db.Text, nullable=False)

  def check_password(self, password):
    return safe_str_cmp(password, "password")


@jwt.user_identity_loader
def user_identity_lookup(user):
  return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
  identity = jwt_data["sub"]
  return User.query.filter_by(id=identity).one_or_none()


@app.route("/login", methods=["POST"])
def login():
  username = request.json.get("username", None)
  password = request.json.get("password", None)

  user = User.query.filter_by(username=username).one_or_none()
  if not user or not user.check_password(password):
    return jsonify("Wrong username or password"), 401
  
  access_token = create_access_token(identity=user)
  return jsonify(access_token=access_token)


@app.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
  return jsonify(
    id=current_user.id,
    full_name=current_user.full_name,
    username=current_user.username,
  )


if __name__ == "__main__":
  db.create_all()
  db.session.add(User(full_name="Seo soosoo_1", username="soosoo_1"))
  db.session.add(User(full_name="Seo soosoo_2", username="soosoo_2"))
  db.session.add(User(full_name="Seo soosoo_3", username="soosoo_3"))
  db.session.commit()

  app.run()
