from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app


app.config.from_object('config')
db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

############################  BOOKS  ###########################
class Book(db.Model):
  __tablename__ = 'books'
  isbn = db.Column(db.Integer, primary_key=True, autoincrement=False)
  title = db.Column(db.String(500), nullable=False)
  author = db.Column(db.String(200), nullable=False)
  year_published = db.Column(db.DATE, nullable=False)
  month_read = db.Column(db.DATE, nullable=False, default=datetime.today())

  def __repr__(self):
      return f'<Book — Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}>'