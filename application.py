import os

import requests
from flask import Flask, render_template, session, request, redirect, url_for, abort, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# Home route
@app.route('/')
def index():
    return render_template('index.html', user_id=session.get('user_id'))

# Registration route
@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        # If method is GET, show user the registration form
        return render_template('register.html', user_id=session.get('user_id'))
    elif request.method == 'POST':
        # If method is POST, check the data
        name = request.form.get('name')
        email = request.form.get('email')
        user_db = db.execute('SELECT * FROM users WHERE name=:name OR email=:email', {'name': name, 'email': email}).fetchone()
        if user_db:
            # If user with specified name or email exists, return to registration page and show alert
            flash('User already exists', 'danger')
            return render_template('register.html', user_id=session.get('user_id'))
        else:
            # If not, save new user credentials in database and show the login page
            db.execute('INSERT INTO users (name, email, password) VALUES (:name, :email, :password)',
                       {'name': name, 'email': email, 'password': generate_password_hash(request.form.get('pass1'))})
            db.commit()
            flash('You have successfully registered! Now you may log in', 'success')
            return render_template('login.html', user_id=session.get('user_id'))

# Login route
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        # If method is GET, just show the page
        return render_template('login.html', show_alert=False, user_id=session.get('user_id'))
    elif request.method == 'POST':
        # If method is POST, check whether the user exists
        name_email = request.form.get('name_email')
        user_db = db.execute('SELECT * FROM users WHERE name=:name_email OR email=:name_email', {'name_email': name_email}).fetchone()
        if not user_db:
            # If the user doesn't exist, return to the login page and show alert
            flash('Wrong credentials', 'danger')
            return render_template('login.html', user_id=session.get('user_id'))
        else:
            if check_password_hash(user_db.password, request.form.get('password')):
                # If the user exists and hashed password is ok, redirect to the search page
                session['user_id'] = user_db.id
                return redirect(url_for('search'))
            else:
                # If not, return back and show alert
                flash('Wrong credentials', 'danger')
                return render_template('login.html', user_id=session.get('user_id'))

# Log out user and return to home page
@app.route('/logout/')
def logout():
    session['user_id'] = None
    return redirect(url_for('index'))

# Search route
@app.route('/search/')
def search():
    if 'query' in request.args:
        # If 'query' is in request arguments, do the search and show results
        query = request.args['query']
        result = db.execute('SELECT * FROM books WHERE isbn ILIKE :pattern OR title ILIKE :pattern OR author ILIKE :pattern ORDER BY id',
                            {'pattern': f'%{query}%'}).fetchall()
        return render_template('search.html', has_query=True, result=result, user_id=session.get('user_id'))
    else:
        # If not, just show the search form
        return render_template('search.html', has_query=False, result=None, user_id=session.get('user_id'))

# Book route
@app.route('/book/<int:book_id>/', methods=['POST', 'GET'])
def book(book_id):
    if request.method == 'GET':
        # If method is GET, get all reviews for this book from database
        logged_in = session.get('user_id') is not None

        reviews = db.execute('SELECT rating, review, users.id, name, email FROM reviews JOIN users ON (users.id = reviews.user_id) WHERE reviews.book_id = :book_id;', {'book_id': book_id}).fetchall()
        already_submit = session.get('user_id') in [review.id for review in reviews]

        book = db.execute('SELECT * FROM books WHERE id = :book_id', {'book_id': book_id}).fetchone()
        gr_data = get_gr_data(book.isbn)

        return render_template('book.html', book=book, user_id=session.get('user_id'), logged_in=logged_in, reviews=reviews, already_submit=already_submit, gr_data=gr_data)
    elif request.method == 'POST':
        # If method is POST, save new review in database
        if session.get('user_id') is None:
            abort(403)
        rating = request.form.get('rating')
        review_text = request.form.get('review')
        db.execute('INSERT INTO reviews (rating, review, user_id, book_id) VALUES (:rating, :review, :user_id, :book_id)',
                   {'rating': rating, 'review': review_text, 'user_id': session.get('user_id'), 'book_id': book_id})
        db.commit()
        return redirect(url_for('book', book_id=book_id))

# API route
@app.route('/api/<isbn>/')
def get_book_by_isbn(isbn):
    books = db.execute('SELECT title, author, year, isbn, rating FROM books LEFT JOIN reviews ON (reviews.book_id = books.id) WHERE isbn = :isbn', {'isbn': isbn}).fetchall()
    if not books:
        abort(404)

    ratings = [book[4] for book in books if book[4] is not None]
    review_count = len(ratings)
    average_score = sum(ratings) / review_count if ratings else 0

    return jsonify({'title': books[0][0],
                    'author': books[0][1],
                    'year': books[0][2],
                    'isbn': books[0][3],
                    'review_count': review_count,
                    'average_score': average_score})

def get_gr_data(isbn):
    """Get GoodRead data."""
    try:
        gr_data_raw = requests.get('https://www.goodreads.com/book/review_counts.json', params={"key": os.getenv("GR_API_KEY"), "isbns": isbn})
    except:
        return None

    try:
        gr_data = gr_data_raw.json()['books'][0]
    except:
        return None

    return gr_data
