from flask import Blueprint

bp = Blueprint('Auth', __name__,url_prefix='/auth')


@bp.route('/login')
def login():
    return 'login'


@bp.route('/register')
def register():
    return 'register'


@bp.route('/profile')
def profile():
    return 'profile'
