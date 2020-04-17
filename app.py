#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import (
    Flask,
    request,
    jsonify,
    abort
)
from models import setup_db, Book, Degree
from flask_cors import CORS
from config import DB_PATH, DB_NAME

from auth import AuthError, requires_auth

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    '''
    Using the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE')
        return response


    ###########################  ROUTES  ############################

    #############  BOOKS  ##############

    '''
        GET /books
            public endpoint
        returns status code 200 and json {"success": True, "total_books": total_books,
        "books": books } where books is a list of book objects,
            or appropriate status code indicating reason for failure
    '''
    @app.route("/books", methods=["GET"])
    def retrieve_books():
        books = Book.query.order_by(Book.date_read).all()
        books = [book.long() for book in books]
        return jsonify({
            "success": True,
            "total_books": len(books),
            "books": books
        })


    '''
        GET /books/id
            public endpoint
        returns status code 200 and json {"success": True, "books": book } where 
        books is an array containing only the matched book object,
            or appropriate status code indicating reason for failure
    '''
    @app.route("/books/<int:id>", methods=["GET"])
    def retrieve_book(id):
        book = Book.query.get(id)
        if book:
            book = book.long()
        else:
            abort(404)
        return jsonify({
            "success": True,
            "books": [book]
        })

        
    '''
        POST /books
            requires the 'post:books' permission
        returns status code 200 and json {"success": True, "books": book} where 
        book is an array containing only the newly created book,
            or appropriate status code indicating reason for failure
    '''
    @app.route("/books", methods=["POST"])
    @requires_auth("post:books")
    def create_book(payload):
        try:
            body = request.get_json()
            new_book = Book(
                isbn=body["isbn"],
                title=body["title"],
                author=body["author"],
                year_published=body["year_published"],
                date_read=body["date_read"]
                )
            new_book.insert()

            return jsonify({
                'success': True,
                'books': [new_book.long()]
            })

        except Exception:
            abort(422)


    '''
        PATCH /books/id
            responds with a 404 error if id is not found
            requires the 'patch:books' permission
        returns status code 200 and json {"success": True, "books": book} where 
        book is an array containing only the updated book,
            or appropriate status code indicating reason for failure
    '''
    @app.route("/books/<int:id>", methods=["PATCH"])
    @requires_auth("patch:books")
    def update_book(payload, id):
        try:
            book = Book.query.get(id)
            data = request.get_json()
            data_keys = list(data.keys())
            book_properties = ["isbn", "title", "author", "year_published", "date_read"]
            if len([k for k in data_keys if k not in book_properties]) > 0:
                raise Exception
            else:
                for key, value in data.items():
                    if value:
                        setattr(book, key, value)

            book.update()
            return jsonify({
                "success": True,
                "books": [book.long()]
            })
        except Exception:
            abort(422)


    '''
        DELETE /books/id
            responds with a 404 error if id is not found
            requires the 'delete:books' permission
        returns status code 200 and json {"success": True, "id_deleted": id} where 
        id is the id of the deleted book record,
            or appropriate status code indicating reason for failure
    '''
    @app.route("/books/<int:id>", methods=["DELETE"])
    @requires_auth("delete:books")
    def delete_book(payload, id):
        try:
            book = Book.query.get(id)
            book.delete()

            return jsonify({
                "success": True,
                "id_deleted": id
            })
        except Exception:
            abort(404)
        


    #############  DEGREES  ##############

    '''
        GET /degrees
            public endpoint
        returns status code 200 and json {"success": True, "total_degrees": total_degrees,
        "degrees": degrees } where degrees is a list of degree objects,
            or appropriate status code indicating reason for failure
    '''
    @app.route("/degrees", methods=["GET"])
    def retrieve_degrees():
        try:
            degrees = Degree.query.order_by(Degree.year_completed).all()
            degrees = [degree.long() for degree in degrees]
            return jsonify({
                "success": True,
                "total_degrees": len(degrees),
                "degrees": degrees
            })
        except Exception:
            abort(400)


    '''
        GET /degrees/id
            public endpoint
        returns status code 200 and json {"success": True, "degrees": degree } where 
        degrees is an array containing only the matched degree object,
            or appropriate status code indicating reason for failure
    '''
    @app.route("/degrees/<int:id>", methods=["GET"])
    def retrieve_degree(id):
        degree = Degree.query.get(id)
        if degree:
            degree = degree.long()
        else:
            abort(404)
        return jsonify({
            "success": True,
            "degrees": [degree]
        })

        
    '''
        POST /degrees
            requires the 'post:degrees' permission
        returns status code 200 and json {"success": True, "degrees": degree} where 
        degree is an array containing only the newly created degree,
            or appropriate status code indicating reason for failure
    '''
    @app.route("/degrees", methods=["POST"])
    @requires_auth("post:degrees")
    def create_degree(payload):
        try:
            body = request.get_json()
            new_degree = Degree(
                institution=body["institution"],
                title=body["title"],
                category=body["category"],
                year_completed=body["year_completed"],
                location=body["location"],
                url=body['url']
                )

            new_degree.insert()

            return jsonify({
                'success': True,
                'degrees': [new_degree.long()]
            })

        except Exception:
            abort(422)


    '''
        PATCH /degrees/id
            responds with a 404 error if id is not found
            requires the 'patch:degrees' permission
        returns status code 200 and json {"success": True, "degrees": degree} where 
        degree is an array containing only the updated degree,
            or appropriate status code indicating reason for failure
    '''
    @app.route("/degrees/<int:id>", methods=["PATCH"])
    @requires_auth("patch:degrees")
    def update_degree(payload, id):
        try:
            degree = Degree.query.get(id)
            data = request.get_json()
            data_keys = list(data.keys())
            degree_properties = ["institution", "title", "category", "year_completed", "url", "location"]
            if len([k for k in data_keys if k not in degree_properties]) > 0:
                raise Exception
            else:
                for key, value in data.items():
                    if value:
                        setattr(degree, key, value)

            degree.update()
            return jsonify({
                "success": True,
                "degrees": [degree.long()]
            })
        except Exception:
            abort(422)


    '''
        DELETE /degrees/id
            responds with a 404 error if id is not found
            requires the 'delete:degrees' permission
        returns status code 200 and json {"success": True, "id_deleted": id} where 
        id is the id of the deleted degree record,
            or appropriate status code indicating reason for failure
    '''
    @app.route("/degrees/<int:id>", methods=["DELETE"])
    @requires_auth("delete:degrees")
    def delete_degree(payload, id):
        try:
            degree = Degree.query.get(id)
            degree.delete()

            return jsonify({
                "success": True,
                "id_deleted": id
            })
        except Exception:
            abort(404)



    ###########################  ERRORS  ############################


    '''
        400 bad request
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad request"
        }), 400


    '''
        404 error handler
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Resource not found"
        }), 404


    '''
        405 error handler
    '''
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Method not allowed"
        }), 405


    '''
        422 unproecssable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable entity"
        }), 422


    '''
        Authentication Error
    '''
    @app.errorhandler(AuthError)
    def handle_bad_request(e):
        return jsonify({
                    "success": False, 
                    "error": e.error['code'],
                    "message": e.error['description'],
                    }), e.status_code
    
    return app

app = create_app()
setup_db(app, DB_PATH + DB_NAME)
