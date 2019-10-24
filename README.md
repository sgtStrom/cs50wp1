## HarvardX CS50W: Web Programming with Python and JavaScript

### Course's link
See [here](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript).

### My certificate
See [here](https://courses.edx.org/certificates/ce24e09f0bb74979b9cfb4535e72d444).

### Requirements
In this project, you’ll build a book review website. Users will be able to register for your website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. You’ll also use the a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via your website’s API.

Alright, it’s time to actually build your web application! Here are the requirements:

  - Registration: Users should be able to register for your website, providing (at minimum) a username and password.
  - Login: Users, once registered, should be able to log in to your website with their username and password.
  - Logout: Logged in users should be able to log out of the site.
  - Import: Provided for you in this project is a file called books.csv, which is a spreadsheet in CSV format of 5000 different books. Each one has an ISBN number, a title, an author, and a publication year. In a Python file called import.py separate from your web application, write a program that will take the books and import them into your PostgreSQL database. You will first need to decide what table(s) to create, what columns those tables should have, and how they should relate to one another. Run this program by running python3 import.py to import the books into your database, and submit this program with the rest of your project code.
  - Search: Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
  - Book Page: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
  - Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
  - Goodreads Review Data: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.
  - API Access: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follow the format:
```
        {
            "title": "Memory",
            "author": "Doug Lloyd",
            "year": 2015,
            "isbn": "1632168146",
            "review_count": 28,
            "average_score": 5.0
        }
```
If the requested ISBN number isn’t in your database, your website should return a 404 error.

  - You should be using raw SQL commands (as via SQLAlchemy’s execute method) in order to make database queries. You should not use the SQLAlchemy ORM (if familiar with it) for this project.
  - In README.md, include a short writeup describing your project, what’s contained in each file, and (optionally) any other additional information the staff should know about your project.
  - If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to requirements.txt!

Beyond these requirements, the design, look, and feel of the website are up to you! You’re also welcome to add additional features to your website, so long as you meet the requirements laid out in the above specification!

### Project 1

My application needs three environment variables to be set:
- `FLASK_APP` - main Flask application file (it is `application.py`)
- `DATABASE_URL` - database URL
- `GR_API_KEY` - Goodread API key

This project includes two Python scripts:
- `application.py`. It contains all Flask view functions
- `import.py`. It saves all data from books.csv into the database.

There are three directories in the project:
  - schemas - contains database's tables schemas
  - static - contains all static files used in project. It in turn contains four subdirectories:
    - images - just one image for a header
    - scripts - contains javascript file for validating passwords
    - style-css - CSS file
    - style-scss - SCSS file
  - templates - templates used in the project
    - layout.html - base HTML templates
    - book.html - book details page
    - index.html - main page
    - login.html - login page
    - register.html - register page
    - search.html - search page.

The project's video: https://www.youtube.com/watch?v=onckguR2GCk
