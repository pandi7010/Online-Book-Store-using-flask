from flask import Flask, render_template, request, redirect
import sqlite3, os

app = Flask(__name__)
DB_FILE = 'books.db'

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        conn.execute('''
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT NOT NULL
            );
        ''')
        sample_data = [
            ("Atomic Habits", "James Clear", "Book"),
            ("Python Crash Course", "Eric Matthes", "Book"),
            ("AI Revolution", "Andrew Ng", "Article"),
            ("Neural Interfaces", "Yann LeCun", "Article"),
            ("Digital Fortress", "Dan Brown", "Book")
        ]
        conn.executemany("INSERT INTO books (title, author, category) VALUES (?, ?, ?)", sample_data)
        conn.commit()
        conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search')
    conn = get_db_connection()
    if search_query:
        books = conn.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + search_query + '%',)).fetchall()
    else:
        books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template('index.html', books=books, search=search_query or '')

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    author = request.form['author']
    category = request.form['category']
    conn = get_db_connection()
    conn.execute("INSERT INTO books (title, author, category) VALUES (?, ?, ?)", (title, author, category))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
