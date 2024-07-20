from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from blog.controller.auth_controller import login_required

bp = Blueprint('Post', __name__, url_prefix='/post')


@bp.route('/posts')
@login_required
def posts():
    from blog.models.modelos import Post
    posts_ = Post.query.all()
    return render_template('admin/posts.html', posts=posts_)


@bp.route('/create_posts', methods=('GET', 'POST'))
@login_required
def create_posts():
    if request.method == 'POST':
        from blog.models.modelos import Post
        from blog import db
        url = request.form.get('url').replace(' ', '-')
        title = request.form.get('title')
        info = request.form.get('info')
        content = request.form.get('ckeditor')
        posts_ = Post(g.user.id, url, title, info, content)

        post_url = Post.query.filter_by(url=url).first()
        if post_url is None:
            db.session.add(posts_)
            db.session.commit()
            flash(f'El blog {posts_.title} se registró correctamente.', 'success')
            return redirect(url_for('Post.posts'))
        else:
            flash(f'EL URL {url} YA ESTÁ REGISTRADO', 'danger')

    return render_template('admin/create.html')


@bp.route('/update_posts/<int:id_>', methods=('GET', 'POST'))
@login_required
def update_posts(id_):
    from blog.models.modelos import Post
    from blog import db

    post = Post.query.get_or_404(id_)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.info = request.form.get('info')
        post.content = request.form.get('ckeditor')
        db.session.commit()
        flash(f'El blog {post.title} se actualizó correctamente.', 'success')
        return redirect(url_for('Post.posts'))

    return render_template('admin/update.html', post=post)


@bp.route('/delete_posts/<int:id_>')
@login_required
def delete_post(id_):
    from blog.models.modelos import Post
    from blog import db

    try:
        post = Post.query.get_or_404(id_)
        post.is_active = 0
        db.session.commit()
        flash(f'El post "{post.title}" ha sido desactivado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Hubo un error al desactivar el post: {str(e)}', 'danger')

    return redirect(url_for('Post.posts'))