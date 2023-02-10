import os

from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__, template_folder='templates')

postgre_password = 'geomatics'
os.environ["DATABASE_URL"] = 'postgresql://postgres:' + postgre_password + '@localhost/lab1'

if not os.getenv('DATABASE_URL'):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# Default Page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        userName = request.form.get('userName')
        pw = request.form.get('pw')
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
    return


if __name__ == '__main__':
    app.run(debug=True)
