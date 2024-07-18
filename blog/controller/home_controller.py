from flask import Blueprint,render_template

bp = Blueprint('Home', __name__)


@bp.route('/')
def index_home():
    return render_template('index.html')


@bp.route('/blog')
def blog_home():
    return render_template('blog.html')
