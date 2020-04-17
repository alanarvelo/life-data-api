# import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Book, Degree
from config import DB_PATH


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


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.db_name = "life_data_test"
        self.db_full_path = DB_PATH + self.db_name
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
        res = self.client().post('/books', json=self.book1)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['books'])

    def test_create_book2(self):
        res = self.client().post('/books', json=self.book2)
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
        res = self.client().patch('/books/1', json={"year_published": "1800"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['books'][0]['year_published'], "1800")

    # @app.route("/books/<int:id>", methods=["DELETE"])
    def test_delete_book(self):
        self.test_create_book1()
        res = self.client().delete('/books/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id_deleted'], 1)
    

    ###################    BOOKS    ###################
    ## Error behavior

    # @app.route("/books", methods=["POST"]) with malformed book
    def test_422_on_create_book(self):
        new_book = self.book1.copy()
        del new_book['title']
        res = self.client().post('/books', json=new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # # @app.route("/books", methods=["POST"]) without JWT token
    # def test_create_book1(self):
    #     res = self.client().post('/books', json=self.book1)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertTrue(data['books'])


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
        res = self.client().patch('/books/1', json={"most_wanted": "2010"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # @app.route("/books", methods=["GET"])
    def test_404_on_delete_book(self):
        res = self.client().delete('/book/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    


















    
    # # @app.route("/books", methods=["POST"]) without JWT token
    # def test_create_book(self):
    #     res = self.client().post('/books', json=self.new_book)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['books'])
    
    # @app.route("/books", methods=["POST"]) with JWT token but wrong book format
    # def test_422_error_on_create_book(self):
    #     new_book = self.new_book
    #     del new_book['title']
    #     res = self.client().post('/books', json=new_book)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False )
    #     self.assertTrue(data['message'], "unprocessable entity")
    
    
    
    # @app.route("/books/<int:id>", methods=["DELETE"])
    # def test_delete_books(self):
    #     res = self.client().delete('/books/{}'.format(self.created_book_id))
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(self.created_book_id, data['id_deleted'])

    


    # # @app.route("/questions", methods=["GET"])
    # def test_get_questions(self):
    #     res = self.client().get('/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'] > 0 )
    #     self.assertTrue(data['categories'])

    # # @app.route("/questions/<int:qid>", methods=["DELETE"])
    # def test_delete_question(self):
    #     res = self.client().delete('/questions/1')
    #     self.assertEqual(res.status_code, 200)

    # # @app.route("/questions", methods=["POST"])
    # def test_add_question(self):
    #     res = self.client().post('/questions', json=self.new_question)

    #     self.assertEqual(res.status_code, 200)

    # # # @app.route("/questions/search", methods=["POST"])
    # def test_questions_search(self):
    #     res = self.client().post('/questions/search', json={"searchTerm": "largest lake in Africa"})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['questions'])
    #     self.assertEqual(data['total_questions'], 1)

    # # @app.route("/categories/<int:cid>/questions", methods=["GET"])
    # def test_questions_per_category(self):
    #     res = self.client().get('/categories/5/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'] > 0)

    # # # @app.route("/quizzes", methods=["POST"])
    # def test_quizz_play(self):
    #     res = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": {"type": "Science", "id": 5}})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['question'])

    # # @app.errorhandler(404)
    # def test_404_on_get_questions(self):
    #     res = self.client().get('/questions?page=500')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False )

    # # @app.errorhandler(405)
    # def test_405_on_add_questions_per_category(self):
    #     res = self.client().post('/categories/5/questions', json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data['success'], False)

    # # @app.errorhandler(422)
    # def test_422_on_quizz_play(self):
    #     res = self.client().post('/quizzes', json={'previous_questions': [], 'id': 5})
    #     data = json.loads(res.data)


    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()