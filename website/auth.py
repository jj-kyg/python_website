from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password1')

    user = User.query.filter_by(username=username).first()
    if user:
      if check_password_hash(user.password, password):
        flash(f'Welcome {user.username}!', category='success')
        login_user(user, remember=True)
        return redirect(url_for('views.todos'))
      else:
        flash('Incorrect Password, please try again', category='error')
    else:
      flash('User account does not exist.', category='error')
  return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'POST':
    email = request.form.get('email')
    username = request.form.get('username')
    password1 = request.form.get('password1')
    confirmPassword = request.form.get('password2')

    user = User.query.filter_by(email=email).first()

    if user:
      flash('User account already exists.', category='error')
    elif password1 != confirmPassword:
      flash('Passwords do not match', category='error')
    elif email == '':
      flash('Please enter correct email', category='error')
    elif username == '':
      flash('Please enter Username', category='error')
    else:
      new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
      db.session.add(new_user)
      db.session.commit()
      flash('Account created! Please login.', category='success')
      return redirect(url_for('views.home'))

  return render_template('sign_up.html')