from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app: Flask = Flask(__name__)

    app.config.from_object('config.Config')
    db.init_app(app)
    from flask_ckeditor import CKEditor

    ckeditor = CKEditor(app)
    import locale
    locale.setlocale(locale.LC_ALL, 'es_ES')

    from blog.controller import home_controller
    app.register_blueprint(home_controller.bp)

    from blog.controller import auth_controller
    app.register_blueprint(auth_controller.bp)

    from blog.controller import post_controller
    app.register_blueprint(post_controller.bp)

    from blog.models.modelos import Post, User
    with app.app_context():
        db.create_all()

    return app
