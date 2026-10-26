Name: Sandra Tobia id 2304045
Name: Manuela Kalaydjian id 2304053


Lab 3  Part II: Library (Books & Authors)
How to Run
1. Set up the MySQL database
mysql -u root -p < problem2_DDL.sqlmysql -u root -p < problem2_DML.sql
2. Install Python dependencies
bash

cd website
pip install -r requirements.txt
3. Change the MySQL password
Open app.py and set your MySQL root password on line 14.

4. Run the website
bash

python app.py
Open http://localhost:5000 in your browser.

Features
F2.1 - View books table (with author_id) and authors table
F2.2 - Add a new book and add a new author
F2.3 - Edit a book and edit an author
F2.4 - Remove a book
F2.5 - Remove an author (CASCADE deletes their books)
Bonus - Upload cover images for books and photos for authors

Database Schema
AUTHOR (author_id INT PK, name VARCHAR, country VARCHAR, photo VARCHAR)
BOOK (book_id INT PK, title VARCHAR, price DECIMAL, author_id FK, cover VARCHAR)
Foreign key: BOOK.author_id references AUTHOR.author_id ON DELETE CASCADE