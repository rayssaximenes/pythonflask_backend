from flask import Flask
from flask_cors import cross_origin, CORS
from flask_migrate import Migrate
from markupsafe import escape
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import smtplib, ssl
from flask import make_response, jsonify


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/library'
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    published_at = db.Column(db.DateTime, unique=True, nullable=False)


class Authors(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)


@app.route('/')
def hello_world():  # put application's code here
    return f'Hello World!'


# @app.route('/rayssa')
# def hello_rayssa():
#     return 'Hello, Rayssa'


@app.route("/<name>") # route parameter /Ximenes,Rayssa
def hello(name):
    return f"Hello, {escape(name)}!"


@app.route('/books/<int:book_id>')
def get_book_by_id(book_id):
    book = Book.query.filter_by(id=book_id).first()
    return {
        "title": book.title,
        "published_at": book.published_at.strftime("%Y-%m-%d"),
        "id": book.id
    }


@app.route('/author/<int:author_id>')
def get_author_by_id(author_id):
    author = Authors.query.filter_by(id=author_id).first()
    if author is None:
        return make_response(jsonify('Not found'), 404)
    return {
        "name": author.name,
        "email": author.email,
        "id": author.id
    }


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book_by_id(book_id):
    book = Book.query.filter_by(id=book_id).first() # [Book(), Book()], Book ,
    db.session.delete(book)
    db.session.commit()
    return f'Removing book {book_id}'

@app.route('/author/<author_id>', methods=['DELETE'])
def delete_author(author_id):
    author = Authors.query.filter_by(id=author_id).first() # [Book(), Book()], Book ,
    db.session.delete(author)
    db.session.commit()
    return f'Removing author {author_id}'

@app.route('/books/<int:book_id>', methods=['PUT'])
@cross_origin()
def update_book_by_id(book_id):
    book = Book.query.filter_by(id=book_id).first()
    book.title = request.json["title"]
    book.published_at = request.json["published_at"]

    db.session.commit()

    return f'Updating book {book_id}'


@app.route('/author/<int:author_id>', methods=['PUT'])
@cross_origin()
def update_author_by_id(author_id):
    author = Authors.query.filter_by(id=author_id).first()
    author.name = request.json["name"]
    author.email = request.json["email"]

    db.session.commit()

    return f'Updating Author {author_id}'



@app.route('/books', methods=['POST'])
@cross_origin()
def insert_book():
    book = Book(title=request.json["title"], published_at=request.json["published_at"])
    db.session.add(book)
    db.session.commit() # insert book(title, published_at) values (valor, vla)

    smtp_server = "localhost"
    port = 1025
    sender_email = "rayssa.librarian@gmail.com"
    password = ''

    server = smtplib.SMTP(smtp_server, port)
    server.sendmail(sender_email, 'librarian@gmail.com', f'Hello, the book {book.title} was created')

    return f' The book {request.json["title"]} was successfully saved'


@app.route('/author', methods=['POST'])
@cross_origin()
def insert_author_email():
    author = Authors(name=request.json["name"], email=request.json["email"])
    db.session.add(author)
    db.session.commit() # insert book(title, published_at) values (valor, vla)
    return f' Author {request.json["name"]} was successfully saved'


@app.route('/books', methods=['GET'])
@cross_origin()
def get_books():
    books = Book.query.all()
    books_list = []
    for book in books:
        books_list.append({"title": book.title, "id": book.id})
    return {
            "books": books_list
        }


@app.route('/authors', methods=['GET'])
@cross_origin()
def get_authors():
    authors = Authors.query.all()
    authors_list = []
    for author in authors:
        authors_list.append({"name": author.name, "email": author.email, "id": author.id})
    return {
        "authors": authors_list
    }
    # books = [
    #     Book(title="ABC"),
    #     Book(title="DEF")
    # ]
    #
    # books = [
    #     {
    #         "title": "ABC"
    #     },
    #     {
    #         "title": "DEF"
    #     }
    # ]



if __name__ == '__main__':
    app.run()
