from flask import Flask, render_template
from models import db, Book
from scraping import scrape_books

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Scraper les livres et les ajouter à la base de données
    books = scrape_books()
    for book in books:
        new_book = Book(title=book['title'], price=book['price'])
        db.session.add(new_book)
    db.session.commit()
    
    # Récupérer les livres de la base de données
    books = Book.query.all()
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
