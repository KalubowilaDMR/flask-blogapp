from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from website import db

views = Blueprint("views", __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Create post success', category='success')
            return redirect(url_for('views.home'))

    return render_template("create_post.html", user=current_user)

@views.route('/delete-post/<id>', methods=['GET'])
@login_required
def delete_post(id):
    if request.method == 'GET':

        post = Post.query.filter_by(id=id).first()

        if not post:
            flash('There no any match post', category='error')
        elif current_user.id != post.author:
            flash('You do not have permission to delete this post', category='error')
        else:
            db.session.delete(post)
            db.session.commit()
            flash('Delete success!', category='success')
        
    return redirect(url_for('views.home'))

@views.route('/post/<username>')
@login_required
def user_post(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Not match username found', category='error')
        return redirect(url_for('views.home'))
    
    posts = user.post
    return render_template('posts.html', user=current_user, posts=posts, username=username)


@views.route('/create-comment/<id>', methods=['POST'])
@login_required
def create_comment(id):
    text = request.form.get('comment')

    if not text:
        flash('Comment cannot be empty!', category='error')
    else:
        post = Post.query.filter_by(id=id).all()

        if post:
            comment = Comment(text=text, author=current_user.id, post_id=id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exists!', category='error')

    return redirect(url_for('views.home'))


@views.route('/delete-comment/<com_id>', methods=['GET'])
@login_required
def del_comment(com_id):
    comm_id = Comment.query.filter_by(id=com_id).first()
    if not comm_id:
        flash('Does not exists matching comment to delete!', category='error')
    elif current_user.id != comm_id.author or current_user.id != comm_id.post.author:
        flash('You dont have permission to delete this comment', category='error')
    else:
        db.session.delete(comm_id)
        db.session.commit()
        flash('Comment Deleted!', category='success')
    return redirect(url_for('views.home'))
    

@views.route('/like/<post_id>', methods=['POST'])
@login_required
def create_like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error' : 'post not exists'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    
    return jsonify({"likes" : len(post.likes), "liked" : current_user.id in map(lambda x: x.author, post.likes)})
        