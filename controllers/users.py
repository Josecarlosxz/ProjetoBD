from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
def list_users():
    return "Lista de usuários"