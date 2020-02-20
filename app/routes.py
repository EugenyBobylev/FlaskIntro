from datetime import datetime
from flask import render_template
from flask_sqlalchemy import Pagination

from app import app, db
from app.forms import LoginForm, PostForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from app.forms import EditProfileForm
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.forms import ResetPasswordForm

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ваше сообщение опубликовано')
        return redirect(url_for('index'))
    # get page of followed posts
    page = request.args.get('page', 1, type=int)
    per_page = app.config['POSTS_PER_PAGE']
    query = current_user.followed_posts()
    page_posts: Pagination = query.paginate(page, per_page, error_out=False)
    posts = page_posts.items
    next_url = url_for('index', page=page_posts.next_num) if page_posts.has_next else None
    prev_url = url_for('index', page=page_posts.prev_num) if page_posts.has_prev else None
    # loging
    app.logger.info('GET /index')
    return render_template('index.html', title='Мой домашний', form=form,
                           posts=posts, next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # get the page of posts
    page = request.args.get('page', 1, type=int)
    per_page = app.config['POSTS_PER_PAGE']
    query = Post.query.filter(Post.user_id == user.id).order_by(Post.timestamp.desc())
    page_posts: Pagination = query.paginate(page, per_page, error_out=False)
    posts = page_posts.items
    next_url = url_for('user', username=user.username, page=page_posts.next_num)\
        if page_posts.has_next else None
    prev_url = url_for('user', username=user.username, page=page_posts.prev_num)\
        if page_posts.has_prev else None
    # logging
    app.logger.info(f'GET /user/{user.username}')
    return render_template('user.html', user=user, posts=posts, prev_url=prev_url, next_url=next_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are following {username}!')
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You are not following {username}.')
    return redirect(url_for('user', username=username))


@app.route('/explore')
@login_required
def explore():
    # get page of followed posts
    page = request.args.get('page', 1, type=int)
    per_page = app.config['POSTS_PER_PAGE']
    query = Post.query.order_by(Post.timestamp.desc())
    page_posts: Pagination = query.paginate(page, per_page, error_out=False)
    posts = page_posts.items
    next_url = url_for('explore', page=page_posts.next_num) if page_posts.has_next else None
    prev_url = url_for('explore', page=page_posts.prev_num) if page_posts.has_prev else None
    # logging
    app.logger.info('GET /explore')

    return render_template('index.html', title="Explore", posts=posts, prev_url=prev_url, next_url=next_url)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
