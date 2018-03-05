from uuid import uuid4
from os import path
from datetime import datetime

from flask import render_template, Blueprint
from sqlalchemy import func

from vergermiya_lightblog.models import db, User, Post, Tag, Comment, posts_tags
from vergermiya_lightblog.forms import CommentForm


blog_blueprint = Blueprint(
    'blog',
    __name__,
    # path.pardir ==> ..
    template_folder=path.join(path.pardir, 'templates', 'blog'),
    # Prefix of Route URL
    url_prefix='/blog')


def sidebar_data():
    """
    Set the sidebar data
    :return: recent data, top tags
    """
    # Get recent post
    recent_post = db.session.query(Post).order_by(
        Post.datetime.desc()).limit(5).all()

    # Get tags
    top_tags = db.session.query(
            Tag, func.count(posts_tags.c.post_id).label("total")
            ).join(posts_tags).group_by(Tag).order_by('total DESC').limit(5).all()

    return recent_post, top_tags


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
@blog_blueprint.route('/index')
def index(page=1):
    """
    index page
    :param page: 1
    :return: template index.html
    """
    posts = Post.query.order_by(Post.datetime.desc()).paginate(page, 10)
    recent_post, top_tags = sidebar_data()
    return render_template('index.html',
                           posts=posts, recent_post=recent_post, top_tags=top_tags)


@blog_blueprint.route('/post/<string:post_id>', methods=['GET', 'POST'])
def post(post_id):
    """
    post page
    :param post_id:
    :return:template post.html
    """

    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(id=str(uuid4()), name=form.name.data)
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        db.session.add(new_comment)
        db.session.commit()

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.datetime.desc()).all()
    recent_post, top_tags = sidebar_data()

    return render_template('post.html',
                           post=post, tags=tags, comments=comments, form=form,
                           recent_post=recent_post, top_tags=top_tags)


@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    """
    tag page
    :param tag_name:
    :return: template tag.html
    """
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.datetime.desc()).all()
    recent_post, top_tags = sidebar_data()

    return render_template('tag.html',
                           tag=tag, posts=posts,
                           recent_post=recent_post, top_tags=top_tags)


@blog_blueprint.route('/user/<string:username>')
def user(username):
    """
    user page
    :param username:
    :return:template user.html
    """
    user = db.session.query(User).filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.datetime.desc()).all()
    recent_post, top_tags = sidebar_data()

    return render_template('user.html',
                           user=user, posts=posts,
                           recent_post=recent_post, top_tags=top_tags)
