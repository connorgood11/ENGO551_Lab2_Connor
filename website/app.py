import os

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
                return render_template('book_search.html')
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
            return render_template('login.html')
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
        query_string = "SELECT * FROM book"
        conditions = []
        if author:
            conditions.append("author=:author")
        if title:
            conditions.append("title=:title")
        if isbn:
            conditions.append("isbn=:isbn")
        if year:
            conditions.append("year=:year")

        # Only add the WHERE clause if there are conditions
        if conditions:
            query_string += " WHERE " + " OR ".join(conditions)

        # Execute the query
        books = db.execute(text(query_string), {"author": author, "title": title, "isbn": isbn, "year": year}).fetchall()

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
