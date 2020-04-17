from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DATE
from datetime import datetime


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, db_full_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_full_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    if 'test' in db_full_path:
        db.drop_all()
        db.create_all()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

############################  BOOKS  ########################### 
class Book(db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    isbn = Column(String(50))
    title = Column(String(500), nullable=False, unique=True)
    author = Column(String(200), nullable=False)
    year_published = Column(String(4))
    date_read = Column(DATE, nullable=False, default=datetime.today())

    '''
    insert()
        inserts a new model into the database
        the model must have a unique isbn & title
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model from the database
        the model must exist in the database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''
    def update(self):
        db.session.commit()

    '''
    long()
        long form representation of the Book model
    '''
    def long(self):
        return {
            'id': self.id,
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'year_published': self.year_published,
            'date_read': self.date_read.strftime('%b %Y'),
        }

    def __repr__(self):
        return f'<Book — Title: {self.title}, Authors: {self.author}, ISBN: {self.isbn}>'

############################  DEGREES  ########################### 
class Degree(db.Model):
    __tablename__ = 'degrees'
    id = Column(Integer, primary_key=True)
    institution = Column(String(200), nullable=False)
    title = Column(String(500), nullable=False, unique=True)
    category = Column(String(50), nullable=False)
    year_completed = Column(String(4), nullable=False)
    location = Column(String(200))
    url = Column(String(1024))

    '''
    insert()
        inserts a new model into the database
        the model must have a unique title
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model from the database
        the model must exist in the database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''
    def update(self):
        db.session.commit()

    '''
    long()
        long form representation of the Degree model
    '''
    def long(self):
        return {
            'id': self.id,
            'institution': self.institution,
            'title': self.title,
            'category': self.category,
            'year_completed': self.year_completed,
            'location': self.location,
            'url': self.url
        }

    def __repr__(self):
        return f'<Degree — Title: {self.title}, Inst.: {self.author}, year: {self.year_completed}>'