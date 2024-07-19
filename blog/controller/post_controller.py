from flask import Blueprint, render_template, request, flash, redirect, url_for, g

bp = Blueprint('Post', __name__, url_prefix='/post')

from blog.controller.auth_controller import login_required


@bp.route('/posts')
@login_required
def posts():
    from blog.models.modelos import Post
    from blog import db
    posts = Post.query.all()

    return render_template('admin/posts.html',posts=posts)


@bp.route('/create_posts')
def create_posts():
    return 'create_posts'


@bp.route('/update_posts')
def update_posts():
    return 'update_posts'
