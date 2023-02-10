import os

from flask import Flask, request, render_template, flash, redirect, url_for
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash

from website import create_app
from website.database import User

app = Flask(__name__, template_folder='templates')
app = create_app()

postgre_password = 'geomatics'
os.environ["DATABASE_URL"] = 'postgresql://postgres:' + postgre_password + '@localhost/lab1'

if not os.getenv('DATABASE_URL'):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# Default Page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        userName = request.form.get('userName')
        pw = request.form.get('pw')
        queryUsername = User.query.filter_by(userName=userName).first()
        if queryUsername:
            print('Username Exists')
            if queryUsername.pw == pw:
                print('Password Correct')
            else:
                print('Password incorrect')
        else:
            print('Username doesnt exist')

    return render_template('login.html')


@app.route('/')
def default():
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        userName = request.form.get('userName')
        pw = request.form.get('pw')
        pw2 = request.form.get('pw2')
        usernameAlreadyExists = User.query.filter_by(userName=userName).first()

        if usernameAlreadyExists:
            flash('Username already exists.', category='error')

        else:
            new_user = User(userName=userName, pw=pw)
            db.session.add(new_user)
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return render_template('login.html')
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
