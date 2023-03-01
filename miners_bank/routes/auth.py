from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from ..database import db_session
from ..models.account import User


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login')
def login():
    return render_template('login.html')

@auth_blueprint.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    stmt = select(User).where(User.email.in_([email]))
    user = db_session.scalars(stmt).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    user.authenticated = True
    db_session.commit()
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth_blueprint.route('/signup')
def signup():
    return render_template('signup.html')

@auth_blueprint.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    stmt = select(User).where(User.email.in_([email]))
    user = db_session.scalars(stmt).first()
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), authenticated=False)

    # add the new user to the database
    db_session.add(new_user)
    db_session.commit()

    return redirect(url_for('auth.login'))

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    current_user.authenticated = False
    db_session.commit()
    return redirect(url_for('main.index'))
