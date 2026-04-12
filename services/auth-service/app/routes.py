from flask import Blueprint, request, jsonify, redirect
from . import db
from .models import User
from authlib.integrations.flask_client import OAuth
import jwt
import datetime
from flask import current_app

auth_bp = Blueprint("auth", __name__)
oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"}
    )

# ── Existing Routes ─────────────────────────────────────────

@auth_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "auth-service healthy"}), 200

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "username, email, and password required"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already taken"}), 409
    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "email and password required"}), 400
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401
    token = jwt.encode(
        {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(
                seconds=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
            )
        },
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )
    return jsonify({"message": "Login successful", "token": token, "user": user.to_dict()}), 200

@auth_bp.route("/verify", methods=["POST"])
def verify_token():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Token missing"}), 401
    try:
        payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        return jsonify({"valid": True, "user": payload}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

# ── Google OAuth Routes ──────────────────────────────────────

@auth_bp.route("/google/login", methods=["GET"])
def google_login():
    redirect_uri = "http://localhost:5001/api/auth/google/callback"
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route("/google/callback", methods=["GET"])
def google_callback():
    token = oauth.google.authorize_access_token()
    user_info = token.get("userinfo")

    if not user_info:
        return jsonify({"error": "Failed to fetch user info from Google"}), 400

    email     = user_info["email"]
    google_id = user_info["sub"]
    name      = user_info.get("name", email.split("@")[0])

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            username=name,
            email=email,
            google_id=google_id,
            auth_provider="google"
        )
        db.session.add(user)
        db.session.commit()

    jwt_token = jwt.encode(
        {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(
                seconds=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
            )
        },
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({
        "message": "Google login successful",
        "token": jwt_token,
        "user": user.to_dict()
    }), 200
