import pandas as pd
import os
from sqlalchemy import create_engine

degrees = pd.read_csv('seed_data/degree_log.csv')
degrees.info()

degrees.drop('Unnamed: 0', axis=1, inplace=True)
degrees.info()

db_url = os.environ.get('DATABASE_URL')
eng = create_engine(db_url)
degrees.to_sql('degrees', con=eng, if_exists='append', index=False)
print("Imported Degrees")



books = pd.read_csv('seed_data/reading_log.csv')
books.info()

books.drop('Unnamed: 0', axis=1, inplace=True)
books.info()

books.isbn.duplicated().sum()
books.drop_duplicates('isbn', inplace=True)
books.isbn.duplicated().sum()


books.year_read.update(books.year_read.astype(str))
books.loc[:, "date_read"] = books.year_read + '-' + books.month_day_read
books.drop(['year_read', 'month_day_read'], axis=1, inplace=True)
books.head()
books.info()

books.isbn.update(books.isbn.astype(str))
books.year_published.update(books.year_published.astype(str))
books.info()

books.to_sql('books', con=eng, if_exists='append', index=False)
print("Imported Books")