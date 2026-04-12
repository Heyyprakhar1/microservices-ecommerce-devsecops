from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password      = db.Column(db.String(255), nullable=True)  # Google users ka nahi hoga
    google_id     = db.Column(db.String(255), unique=True, nullable=True)
    auth_provider = db.Column(db.String(20), default="local")  # "local" or "google"

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        # Google user ne password se login karne ki koshish ki toh block karo
        if self.auth_provider == "google":
            return False
        return check_password_hash(self.password, raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "auth_provider": self.auth_provider
        }
