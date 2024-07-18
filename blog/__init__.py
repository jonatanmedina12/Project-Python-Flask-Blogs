from flask import Flask


def create_app():
    app = Flask(__name__)

    from blog.controller import home_controller
    app.register_blueprint(home_controller.bp)

    from blog.controller import auth_controller
    app.register_blueprint(auth_controller.bp)

    from blog.controller import post_controller
    app.register_blueprint(post_controller.bp)

    return app
