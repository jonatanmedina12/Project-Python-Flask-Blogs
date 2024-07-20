from functools import wraps
from flask import Blueprint, render_template, request, url_for, g, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

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
            flash(error, 'danger')
        else:
            users = User.query.filter_by(email=email).first()
            if users is None or not check_password_hash(users.password, password):
                error = 'Correo o contraseña incorrecta'
                flash(error, 'danger')

            if error is None:
                session.clear()
                session['user_id'] = users.id
                flash('Inicio de sesión exitoso.', 'success')
                return redirect(url_for('Post.posts'))

    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    from blog.models.modelos import User
    from blog import db

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if username is None or password is None or email is None:
            error = 'Campos obligatorios'
            flash(error, 'danger')

        users = User(username, generate_password_hash(password), email, None)

        user_email = User.query.filter_by(email=email).first()
        if user_email is None:
            db.session.add(users)
            db.session.commit()
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            error = f'El correo {email} ya está registrado'
            flash(error, 'danger')

    return render_template('auth/register.html')


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.get('user') is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@bp.route('/profile/<int:id>', methods=('GET', 'POST'))
@login_required
def profile(id_):
    from blog.models.modelos import User
    from blog import db
    user = User.query.get_or_404(id_)
    error = None
    if request.method == 'POST':
        user.username = request.form.get('username')
        password = request.form.get('password')

        if len(password) != 0:
            if len(password) < 6:
                error = 'La contraseña debe tener más de 5 caracteres'
                flash(error, 'danger')
            else:
                user.password = generate_password_hash(password)
        if request.files['photo']:
            photo = request.files['photo']
            photo.save(f'blog/static/media/{secure_filename(photo.filename)}')
            user.photo = f'media/{secure_filename(photo.filename)}'

        if error is not None:
            flash(error, 'danger')
        else:
            db.session.commit()
            flash('Perfil actualizado correctamente.', 'success')
            return redirect(url_for('auth.profile', id=user.id))

    return render_template('auth/profile.html', user=user)


@bp.route('/logout')
def logout():
    session.clear()
    flash('Cierre de sesión exitoso.', 'success')
    return redirect(url_for('home.index_home'))


@bp.before_app_request
def load_logger_in_user():
    from blog.models.modelos import User

    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)
