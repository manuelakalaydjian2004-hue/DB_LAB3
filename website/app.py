from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'lab3_secret_key_2026'

# MySQL connection config 
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1111',  
    'database': 'library'
}

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ==================== HOME / BOOKS ====================

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM BOOK ORDER BY book_id")
    books = cursor.fetchall()
    cursor.execute("SELECT * FROM AUTHOR ORDER BY author_id")
    authors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', books=books, authors=authors, tab='books')


@app.route('/authors')
def authors_page():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM AUTHOR ORDER BY author_id")
    authors = cursor.fetchall()
    for a in authors:
        cursor.execute("SELECT COUNT(*) as cnt FROM BOOK WHERE author_id = %s", (a['author_id'],))
        result = cursor.fetchone()
        a['book_count'] = result['cnt']
    cursor.execute("SELECT * FROM BOOK ORDER BY book_id")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', books=books, authors=authors, tab='authors')


# ==================== ADD AUTHOR ====================

@app.route('/authors/add', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        author_id = request.form['author_id']
        name = request.form['name']
        country = request.form.get('country', '') or None
        photo = None

        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"author_{author_id}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'authors', filename)
                file.save(filepath)
                photo = f"uploads/authors/{filename}"

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO AUTHOR (author_id, name, country, photo) VALUES (%s, %s, %s, %s)",
                (author_id, name, country, photo)
            )
            conn.commit()
            flash('Author added successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('authors_page'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(author_id) as max_id FROM AUTHOR")
    result = cursor.fetchone()
    next_id = (result[0] or 0) + 1
    cursor.close()
    conn.close()
    return render_template('add_author.html', next_id=next_id)


# ==================== EDIT AUTHOR ====================

@app.route('/authors/edit/<int:author_id>', methods=['GET', 'POST'])
def edit_author(author_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        country = request.form.get('country', '') or None
        photo = request.form.get('current_photo') or None

        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"author_{author_id}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'authors', filename)
                file.save(filepath)
                photo = f"uploads/authors/{filename}"

        if request.form.get('remove_photo'):
            photo = None

        try:
            cursor.execute(
                "UPDATE AUTHOR SET name=%s, country=%s, photo=%s WHERE author_id=%s",
                (name, country, photo, author_id)
            )
            conn.commit()
            flash('Author updated successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('authors_page'))

    cursor.execute("SELECT * FROM AUTHOR WHERE author_id = %s", (author_id,))
    author = cursor.fetchone()
    cursor.close()
    conn.close()
    if not author:
        flash('Author not found!', 'error')
        return redirect(url_for('authors_page'))
    return render_template('edit_author.html', author=author)


# ==================== DELETE AUTHOR (CASCADE) ====================

@app.route('/authors/delete/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) as cnt FROM BOOK WHERE author_id = %s", (author_id,))
        book_count = cursor.fetchone()['cnt']

        cursor.execute("DELETE FROM AUTHOR WHERE author_id = %s", (author_id,))
        conn.commit()
        flash(f'Author deleted! {book_count} book(s) were also removed (CASCADE).', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('authors_page'))


# ==================== ADD BOOK ====================

@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        title = request.form['title']
        price = request.form.get('price', '') or None
        author_id = request.form.get('author_id', '') or None
        cover = None

        if 'cover' in request.files:
            file = request.files['cover']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"book_{book_id}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'books', filename)
                file.save(filepath)
                cover = f"uploads/books/{filename}"

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO BOOK (book_id, title, price, author_id, cover) VALUES (%s, %s, %s, %s, %s)",
                (book_id, title, price, author_id, cover)
            )
            conn.commit()
            flash('Book added successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('index'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT MAX(book_id) as max_id FROM BOOK")
    result = cursor.fetchone()
    next_id = (result['max_id'] or 0) + 1
    cursor.execute("SELECT * FROM AUTHOR ORDER BY author_id")
    authors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_book.html', next_id=next_id, authors=authors)


# ==================== EDIT BOOK ====================

@app.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        price = request.form.get('price', '') or None
        author_id = request.form.get('author_id', '') or None
        cover = request.form.get('current_cover') or None

        if 'cover' in request.files:
            file = request.files['cover']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"book_{book_id}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'books', filename)
                file.save(filepath)
                cover = f"uploads/books/{filename}"

        if request.form.get('remove_cover'):
            cover = None

        try:
            cursor.execute(
                "UPDATE BOOK SET title=%s, price=%s, author_id=%s, cover=%s WHERE book_id=%s",
                (title, price, author_id, cover, book_id)
            )
            conn.commit()
            flash('Book updated successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM BOOK WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.execute("SELECT * FROM AUTHOR ORDER BY author_id")
    authors = cursor.fetchall()
    cursor.close()
    conn.close()
    if not book:
        flash('Book not found!', 'error')
        return redirect(url_for('index'))
    return render_template('edit_book.html', book=book, authors=authors)


# ==================== DELETE BOOK ====================

@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM BOOK WHERE book_id = %s", (book_id,))
        conn.commit()
        flash('Book deleted successfully!', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)