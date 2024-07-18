from flask import Blueprint

bp = Blueprint('Post', __name__,url_prefix='/post')


@bp.route('/posts')
def posts():
    return 'posts'


@bp.route('/create_posts')
def create_posts():
    return 'create_posts'


@bp.route('/update_posts')
def update_posts():
    return 'update_posts'
