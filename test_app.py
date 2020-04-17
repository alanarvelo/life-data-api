import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Book, Degree
from config import JWT

active_auth={"Authorization": "Bearer {}".format(JWT)}

class BookTestCase(unittest.TestCase):
    """This class represents the Book test case"""

    book1 = {
        "title": "No Filter: The Inside Story of Instagram",
        "author": "Sarah Frier",
        "isbn": "9781982126803",
        "year_published": "2020",
        "date_read": "2020-05-01"
    }
    book2 = {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "isbn": "9780446310789",
        "year_published": "1960",
        "date_read": "2020-06-01"
    }
    degree1 = {
        "category": "Course",
        "institution": "Udacity",
        "location": "Online",
        "title": "Cloud Developer",
        "url": None,
        "year_completed": "2020"
    }
    degree2 = {
        "category": "Course",
        "institution": "Udacity",
        "location": "Online",
        "title": "Data Structures and Algorithms",
        "url": None,
        "year_completed": "2020"
    }


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.db_name = "life_data_test"
        self.db_full_path = os.environ.get('DATABASE_URL_TEST')
        setup_db(self.app, self.db_full_path)
        
    
    def tearDown(self):
        """Executed after reach test"""
        # pass

    """
        TESTS
    """

    ###################    BOOKS    ###################
    ## Regular behavior

    # @app.route("/books", methods=["POST"]) with JWT token
    def test_create_book1(self):
        res = self.client().post('/books', json=self.book1, headers=active_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['books'])


    def test_create_book2(self):
        res = self.client().post('/books', json=self.book2, headers=active_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['books'])


    # @app.route("/books/<int:id>", methods=["GET"])
    def test_get_book(self):
        self.test_create_book1()
        res = self.client().get('/books/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['books'])


    # @app.route("/books", methods=["GET"])
    def test_get_books(self):
        self.test_create_book1()
        self.test_create_book2()
        res = self.client().get('/books')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['books']), 2)

    
    # @app.route("/books/<int:id>", methods=["PATCH"])
    def test_patch_book(self):
        self.test_create_book1()
        res = self.client().patch('/books/1', json={"year_published": "1800"}, headers=active_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['books'][0]['year_published'], "1800")

    # @app.route("/books/<int:id>", methods=["DELETE"])
    def test_delete_book(self):
        self.test_create_book1()
        res = self.client().delete('/books/1', headers=active_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id_deleted'], 1)
    

    ###################    BOOKS    ###################
    ## Error behavior

    # @app.route("/books", methods=["POST"]) with JWT token but malformed book
    def test_422_on_create_book(self):
        new_book = self.book1.copy()
        del new_book['title']
        res = self.client().post('/books', json=new_book, headers=active_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    # @app.route("/books/<int:id>", methods=["GET"])
    def test_404_on_get_book(self):
        self.test_create_book1()
        res = self.client().get('/books/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    # @app.route("/books", methods=["GET"])
    def test_404_on_get_books(self):
        res = self.client().get('/booksS')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    

    # @app.route("/books", methods=["GET"])
    def test_405_on_get_books(self):
        res = self.client().patch('/books')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    
    # @app.route("/books/<int:id>", methods=["PATCH"])
    def test_422_on_patch_book(self):
        self.test_create_book1()
        res = self.client().patch('/books/1', json={"most_wanted": "2010"}, headers=active_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    # @app.route("/books", methods=["GET"])
    def test_404_on_delete_book(self):
        res = self.client().delete('/book/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    ## Not Authorized behavior

    # @app.route("/books", methods=["POST"]) without JWT token
    def test_not_auth_on_create_book1(self):
        res = self.client().post('/books', json=self.book1)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    

    # @app.route("/books/<int:id>", methods=["PATCH"])
    def test_not_auth_on_patch_book(self):
        self.test_create_book1()
        res = self.client().patch('/books/1', json={"most_wanted": "2010"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    
    # @app.route("/books/<int:id>", methods=["DELETE"])
    def test_not_auth_on_delete_book(self):
        self.test_create_book1()
        res = self.client().delete('/books/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)



    ###################    DEGREE    ###################
    ## Regular behavior

    # @app.route("/degrees", methods=["POST"]) with JWT token
    def test_create_degree1(self):
        res = self.client().post('/degrees', json=self.degree1, headers=active_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['degrees'])


    def test_create_degree2(self):
        res = self.client().post('/degrees', json=self.degree2, headers=active_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['degrees'])


    # @app.route("/degrees/<int:id>", methods=["GET"])
    def test_get_degree(self):
        self.test_create_degree1()
        res = self.client().get('/degrees/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['degrees'])


    # @app.route("/degrees", methods=["GET"])
    def test_get_degrees(self):
        self.test_create_degree1()
        self.test_create_degree2()
        res = self.client().get('/degrees')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['degrees']), 2)

    
    # @app.route("/degrees/<int:id>", methods=["PATCH"])
    def test_patch_degree(self):
        self.test_create_degree1()
        res = self.client().patch('/degrees/1', json={"year_completed": "2000"}, headers=active_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['degrees'][0]['year_completed'], "2000")

    # @app.route("/degrees/<int:id>", methods=["DELETE"])
    def test_delete_degree(self):
        self.test_create_degree1()
        res = self.client().delete('/degrees/1', headers=active_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id_deleted'], 1)
    

    ###################    DEGREES    ###################
    ## Error behavior

    # @app.route("/degrees", methods=["POST"]) with JWT token but malformed degree
    def test_422_on_create_degree(self):
        new_degree = self.degree1.copy()
        del new_degree['title']
        res = self.client().post('/degrees', json=new_degree, headers=active_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    # @app.route("/degrees/<int:id>", methods=["GET"])
    def test_404_on_get_degree(self):
        self.test_create_degree1()
        res = self.client().get('/degrees/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    # @app.route("/degrees", methods=["GET"])
    def test_404_on_get_degrees(self):
        res = self.client().get('/degreesS')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    

    # @app.route("/degrees", methods=["GET"])
    def test_405_on_get_degrees(self):
        res = self.client().patch('/degrees')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    
    # @app.route("/degrees/<int:id>", methods=["PATCH"])
    def test_422_on_patch_degree(self):
        self.test_create_degree1()
        res = self.client().patch('/degrees/1', json={"most_wanted": "2010"}, headers=active_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    # @app.route("/degrees", methods=["GET"])
    def test_404_on_delete_degree(self):
        res = self.client().delete('/degree/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    ## Not Authorized behavior

    # @app.route("/degrees", methods=["POST"]) without JWT token
    def test_not_auth_on_create_degree1(self):
        res = self.client().post('/degrees', json=self.degree1)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    

    # @app.route("/degrees/<int:id>", methods=["PATCH"])
    def test_not_auth_on_patch_degree(self):
        self.test_create_degree1()
        res = self.client().patch('/degrees/1', json={"most_wanted": "2010"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    
    # @app.route("/degrees/<int:id>", methods=["DELETE"])
    def test_not_auth_on_delete_degree(self):
        self.test_create_degree1()
        res = self.client().delete('/degrees/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()