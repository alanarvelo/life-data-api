# Personal website backend

### URL
This application is currently hosted at `www.alanarvelo.com/data`

## Getting Started

### Installing Dependencies

**Python 3.7** is required. A virtual environment is encouraged. Dependencies can be installed by running the below command form the root directory:

```bash
pip install -r requirements.txt
```

##### Key Dependencies
- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

##### Database Setup
To test locally you must create a sql database, I use postgres, and add the `DATABASE_URL` as an environment variable. This will be used in `app.py` via os.environ.get() to connect yo your local db.

Then, from within the `backend/` directory, you can run the database migration by:
```bash
python manage.py db upgrade
```
To fill your local database, create some dummy data and run:
```bash
python import_data.py
```


##### Running the server

From within the `backend/` directory, first ensure you are working using your created virtual environment.

To run the server, execute:
```bash
export FLASK_APP=app.py
export FLASK_DEBUG=true
flask run
```
Setting the `FLASK_APP` variable to `app.py` directs flask to this file to find the application.


### Roles & Permissions
The API handles 2 collections `books` and `degrees`, each supports CRUD methods as to be seen below in *API Reference*. Read operations are of public access by sending `GET` requests to their respective endpoints. Create, update, and delete operations require authentication.

There are 2 roles:
+ **book_reader** has permissions `post:books`, `patch:books`, and `delete:books`.
+ **degrees_reader** has permissions `degrees:books`, `degrees:books`, and `degrees:books`.

The roles above are required to perform `post`, `patch`, `delete`, actions. Shoot me an email if you want access.

## API Reference

### Getting Started
- Base URL: currently the server runs locally on `http://127.0.0.1:5000/` and live on `www.alanarvelo.com/data`.
- Authentication: read above.

### Error Handling
Flask's `@app.errorhandler` decorator is implemented for:
- 400: Bad request
- 401: Unauthorized
- 404: Resource not found
- 405: Method not allowed
- 422: Unprocessable entity

Errors return JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "Resource not found"
}
```


### Endpoints 

### Books

#### GET /books
- General:
    - Returns a list of books, the total number of books, and a success value. 
    - Public endpoint
- Sample: `curl http://127.0.0.1:5000/books`
```
   "books":[
        {
            "author": "Pedro McKinney",
            "date_read": "Jan 2019",
            "id": 32,
            "isbn": "0",
            "title": "El año que vivimos en peligro",
            "year_published": "2005"
        },
        {
            "author": "Dale Carnegie",
            "date_read": "Mar 2017",
            "id": 3,
            "isbn": "9780671723651",
            "title": "How to Win Friends and Influence People",
            "year_published": "1936"
        }
        ...,
   ],
   "success":true,
   "total_books":19
}
```

#### GET /books/{book_id}
- General:
    - Returns a list with the book requested, and a success value. 
    - Public endpoint
- Sample: `curl http://127.0.0.1:5000/books/32`
```
   "books":[
        {
            "author": "Pedro McKinney",
            "date_read": "Jan 2019",
            "id": 32,
            "isbn": "0",
            "title": "El año que vivimos en peligro",
            "year_published": "2005"
        }
   ],
   "success":true
}
```

#### POST /books/
- General:
    - Creates a new book resource using the submitted book object. Returns a list with the newly create book resource and a success value.
    - Requires authentication and the `post:books` permission.
- Sample: `curl http://127.0.0.1:5000/books? -X POST -H "Content-Type: application/json" -d '{"title": "No Filter: The Inside Story of Instagram", "author": "Sarah Frier", "isbn": "9781982126803", "year_published": "2020", "date_read": "2020-05-01"}'`
```
   "books":[
        {
            "id": 60
            "title": "No Filter: The Inside Story of Instagram",
            "author": "Sarah Frier",
            "isbn": "9781982126803",
            "year_published": "2020",
            "date_read": "2020-05-01"
        }
   ],
   "success":true
}
```

#### PATCH /books/{bood_id}
- General:
    - Updates an existing book resource using the submitted book property object. Returns a list with the updated book resource and a success value.
    - Requires authentication and the `patch:books` permission.
- Sample: `curl http://127.0.0.1:5000/books/60? -X POST -H "Content-Type: application/json" -d '{"title": "No Filter: No subtitle"}'`
```
   "books":[
        {
            "id": 60,
            "title": "No Filter: The Inside Story of Instagram",
            "author": "Sarah Frier",
            "isbn": "9781982126803",
            "year_published": "2020",
            "date_read": "2020-05-01"
        }
   ],
   "success":true
}
```


#### DELETE /books/{book_id}
- General:
    - Deletes the book of the given ID if it exists. Returns the id of the deleted book and a success value. 
    -  Requires authentication and the `delete:books` permission.
- Sample: `curl -X DELETE http://127.0.0.1:5000/books/3`
```
{
    "id_deleted":3,
    "success":true
}
```


### Degrees

#### GET /degrees
- General:
    - Returns a list of degrees, the total number of degrees, and a success value. 
    - Public endpoint
- Sample: `curl http://127.0.0.1:5000/degrees`
```
   "degrees":[
        {
            "category": "MS",
            "id": 2,
            "institution": "KTH Royal Institute of Techonology",
            "location": "Stockholm, Sweden",
            "title": "Master of Science in Electrical Engineering",
            "url": "http://www.alanarvelo.com/resources/degrees/alan_arvelo_kth_ms_degree.pdf",
            "year_completed": "2017"
        },
        {
            "category": "Course",
            "id": 6,
            "institution": "Udacity",
            "location": "Online",
            "title": "React",
            "url": "https://graduation.udacity.com/confirm/9H7TT4HG",
            "year_completed": "2019"
        }
        ...,
   ],
   "success":true,
   "total_degrees":8
}
```

#### GET /degrees/{degree_id}
- General:
    - Returns a list with the degree requested, and a success value. 
    - Public endpoint
- Sample: `curl http://127.0.0.1:5000/degrees/6`
```
   "degrees":[
        {
            "category": "Course",
            "id": 6,
            "institution": "Udacity",
            "location": "Online",
            "title": "React",
            "url": "https://graduation.udacity.com/confirm/9H7TT4HG",
            "year_completed": "2019"
        }
   ],
   "success":true
}
```

#### POST /degrees/
- General:
    - Creates a new degree resource using the submitted degree object. Returns a list with the newly create degree resource and a success value.
    - Requires authentication and the `post:degrees` permission.
- Sample: `curl http://127.0.0.1:5000/degrees? -X POST -H "Content-Type: application/json" -d '{"category": "Course", "institution": "Udacity", "location": "Online", "title": "Cloud Developer", "url": None, "year_completed": "2020"}'`
```
   "degrees":[
        {
            "id": "9",
            "category": "Course",
            "institution": "Udacity",
            "location": "Online",
            "title": "Cloud Developer",
            "url": None,
            "year_completed": "2020"
        }
   ],
   "success":true
}
```

#### PATCH /degrees/{bood_id}
- General:
    - Updates an existing degree resource using the submitted degree property object. Returns a list with the updated degree resource and a success value.
    - Requires authentication and the `patch:degrees` permission.
- Sample: `curl http://127.0.0.1:5000/degrees/9? -X POST -H "Content-Type: application/json" -d '{"title": "Data Structures and Algorithms"}'`
```
   "degrees":[
        {
            "id": "9",
            "category": "Course",
            "institution": "Udacity",
            "location": "Online",
            "title": "Data Structures and Algorithms",
            "url": None,
            "year_completed": "2020"
        }
   ],
   "success":true
}
```


#### DELETE /degrees/{degree_id}
- General:
    - Deletes the degree of the given ID if it exists. Returns the id of the deleted degree and a success value. 
    -  Requires authentication and the `delete:degrees` permission.
- Sample: `curl -X DELETE http://127.0.0.1:5000/degrees/9`
```
{
    "id_deleted":9,
    "success":true
}
```
