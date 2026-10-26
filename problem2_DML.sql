USE library;

INSERT INTO author (name, country, photo) VALUES ('J.K. Rowling', 'United Kingdom', NULL);
INSERT INTO author (name, country, photo) VALUES ('Stephen King', 'United States', NULL);
INSERT INTO author (name, country, photo) VALUES ('Naguib Mahfouz', 'Egypt', NULL);

INSERT INTO book (title, price, author_id, cover) VALUES ('Harry Potter and the Philosophers Stone', 25.50, 1, NULL);
INSERT INTO book (title, price, author_id, cover) VALUES ('Harry Potter and the Chamber of Secrets', 28.00, 1, NULL);
INSERT INTO book (title, price, author_id, cover) VALUES ('The Shining', 22.00, 2, NULL);
INSERT INTO book (title, price, author_id, cover) VALUES ('IT', 30.00, 2, NULL);
INSERT INTO book (title, price, author_id, cover) VALUES ('Midaq Alley', 18.00, 3, NULL);
INSERT INTO book (title, price, author_id, cover) VALUES ('Cairo Trilogy', 35.00, 3, NULL);