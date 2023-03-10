import os
from functools import wraps

from flask import Flask, request, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash

from website import create_app
from website.database import User

postgre_password = 'geomatics'
app = create_app(postgre_password)

os.environ["DATABASE_URL"] = 'postgresql://postgres:' + postgre_password + '@localhost/lab1'

if not os.getenv('DATABASE_URL'):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
session = db()


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
                # session['logged_in'] = True
                login_user(User(userName=userName, pw=pw), remember=True)
                return render_template('book_search.html')
            else:
                print('Password incorrect')
        else:
            print('Username doesnt exist')

    return render_template('login.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)

    return decorated_function


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
            print('username already exists')
            return render_template('signup.html')
        elif pw != pw2:
            print('the passwords do not match')
            return render_template('signup.html')
        else:
            new_user = User(userName=userName, pw=pw)
            db.add(new_user)
            db.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return render_template('book_search.html')
    return render_template('signup.html')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def book_search():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        year = request.form.get('year')

        # Build the query string based on the form inputs
        query_string = "SELECT * FROM books"
        conditions = []
        print(author)
        if author:
            conditions.append("author LIKE :author")
        if title:
            conditions.append("title LIKE :title")
        if isbn:
            conditions.append("isbn LIKE :isbn")
        if year:
            conditions.append("year = " + str(year))

        # Only add the WHERE clause if there are conditions
        if conditions:
            query_string += " WHERE " + " AND ".join(conditions)

        # Execute the query
        print(query_string)
        books = db.execute(text(query_string), {"author": f'%{author}%', "title": f'%{title}%', "isbn": f'%{isbn}%', "year": {year}}).fetchall()
        print(books)
        if not books:
            flash('No books found!')
        return render_template('book_search.html', books=books)

    return render_template('book_search.html')


@app.route('/logout')
def logout():
    logout_user()
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run(debug=True)
