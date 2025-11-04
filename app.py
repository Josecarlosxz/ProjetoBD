from flask import Flask
import secrets
from flask_login import LoginManager
from models import User

from controllers import user_bp

app.register_blueprint(user_bp)
app.register_blueprint(product_bp)

secret_key = secrets.token_urlsafe(32)

app = Flask(__name__)
app.secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

