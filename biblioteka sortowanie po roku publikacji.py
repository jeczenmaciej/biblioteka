from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer)
    isbn = db.Column(db.String(13), unique=True)

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    publication_year = fields.Int()
    isbn = fields.Str()

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify(books_schema.dump(books))

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book_schema.dump(book))

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(**data)
    db.session.add(new_book)
    db.session.commit()
    return jsonify(book_schema.dump(new_book)), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.json
    for key, value in data.items():
        setattr(book, key, value)
    db.session.commit()
    return jsonify(book_schema.dump(book))

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route('/books/sort/year', methods=['GET'])
def sort_books_by_year():
    books = Book.query.order_by(Book.publication_year.desc()).all()
    return jsonify(books_schema.dump(books))