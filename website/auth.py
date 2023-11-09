from flask import Blueprint, render_template, redirect, url_for, request, flash
from website import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user :
            if check_password_hash(user.password, password):
                flash('Loggedin Success!', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email address does not exists!', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':

        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password")
        password2 = request.form.get("againPassword")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email already use. Try another', category='error')
        elif username_exists:
            flash('Username already use', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short', category='error')
        elif len(email) < 4:
            flash('Email is invalid', category='error')
        elif len(password1) < 7:
            flash('Password is too short', category='error')
        else:
            hash_pasword = generate_password_hash(password1, method="scrypt", salt_length=16)
            new_user = User(email=email, username=username, password=hash_pasword)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('New user created!', category='success')
            print(hash_pasword)
            return redirect(url_for('auth.login'))
        
    return render_template("signup.html", user=current_user)

@auth.route('/sign-out')
@login_required
def log_out():
    logout_user()
    return redirect(url_for("views.home"))