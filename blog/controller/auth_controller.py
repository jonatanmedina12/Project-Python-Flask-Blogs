from functools import wraps

from flask import Blueprint, render_template, request, url_for, g, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        from blog.models.modelos import User
        from blog import db
        email = request.form.get('email')
        password = request.form.get('password')

        error = None
        if email == "" or password == "":
            error = 'Campos Vacíos'
        else:
            users = User.query.filter_by(email=email).first()
            if users is None or not check_password_hash(users.password, password):
                error = 'Correo o contraseña incorrecta'

            if error is None:
                session.clear()
                session['user_id'] = users.id
                return redirect(url_for('Post.posts'))
        flash(error)

    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    from blog.models.modelos import User
    from blog import db
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if username is None or password is None or email is None:
            error = 'Campos obligatorios'
            flash(error)

        users = User(username, generate_password_hash(password), email, None)

        user_email = User.query.filter_by(email=email).first()
        if user_email is None:
            db.session.add(users)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El correo {email} ya esta registrado'
        flash(error)

    return render_template('auth/register.html')


@bp.route('/profile')
def profile():
    return 'profile'


@bp.before_app_request
def load_logger_in_user():
    from blog.models.modelos import User

    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('Home.index'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.get('user') is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
