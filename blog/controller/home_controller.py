from flask import Blueprint, render_template, redirect, request, url_for

bp = Blueprint('home', __name__)


def get_user(id_):
    from blog.models.modelos import User
    user = User.query.get_or_404(id_)
    return user


def search_posts(query):
    from blog.models.modelos import Post
    posts = Post.query.filter(Post.title.ilike(f'%{query}%')).all()
    return posts


@bp.route('/', methods=('GET', 'POST'))
def index_home():
    from blog.models.modelos import Post
    posts = Post.query.all()

    value = None
    if request.method == 'POST':
        query = request.form.get('search')
        posts = search_posts(query)
        value = 'hidden'

    return render_template('index.html', posts=posts, get_user=get_user, value=value)


@bp.route('/blog/<url>')
def blog_home(url):
    from blog.models.modelos import Post
    posts = Post.query.filter_by(url=url).first()
    return render_template('blog.html', posts=posts, get_user=get_user)
