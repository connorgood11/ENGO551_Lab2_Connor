from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_session import Session
from .database import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userName = request.form.get('userName')
        pw = request.form.get('pw')

        userName = User.query.filter_by(userName=userName).first()
        if userName:
            if session['logged_in'] = True:
                flash('Logged in successfully!', category='success')
                login_user(userName, remember=True)
                return redirect(url_for('views.homepage'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        userName = request.form.get('userName')
        pw = request.form.get('pw')
        pw2 = request.form.get('pw2')

        userName = User.query.filter_by(userName=userName).first()
        if userName:
            flash('username already exists.', category='error')

        else:
            new_user = User(userName=userName, pw=generate_password_hash(pw, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.homepage'))

    return render_template("sign_up.html", user=current_user)


