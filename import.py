"""
Import all data from books.csv into database.
"""
import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


CSV_FILE = 'books.csv'

engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

if __name__ == '__main__':
    print('Begin reading data from file...')
    with open(CSV_FILE, 'r') as f:
        reader = csv.reader(f)
        count = 0
        for isbn, title, author, year in reader:
            db.execute('INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)',
                        {'isbn': isbn, 'title': title, 'author': author, 'year': year})
            count += 1
            if count % 100 == 0:
                print(f'{count} records done')
        print('Make commit...')
        db.commit()
        print('Done')
