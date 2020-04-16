from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app


app.config.from_object('config')
db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

############################  BOOKS  ########################### https://www.goodreads.com/book/isbn/
class Book(db.Model):
  __tablename__ = 'books'
  isbn = db.Column(db.String(50), primary_key=True, autoincrement=False)
  title = db.Column(db.String(500), nullable=False)
  author = db.Column(db.String(200), nullable=False)
  year_published = db.Column(db.String(4), nullable=False)
  date_read = db.Column(db.DATE, nullable=False, default=datetime.today())

  def __repr__(self):
      return f'<Book — Title: {self.title}, Authors: {self.author}, ISBN: {self.isbn}>'