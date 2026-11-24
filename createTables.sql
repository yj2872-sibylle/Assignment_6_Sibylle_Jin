-- Reel & Frame Books: a film and media bookstore
-- Creates the category and book tables.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS category;

CREATE TABLE category (
    categoryId          INTEGER PRIMARY KEY,
    categoryName        TEXT    NOT NULL UNIQUE,
    categoryDescription TEXT    NOT NULL,
    categoryImage       TEXT    NOT NULL
);

CREATE TABLE book (
    bookId      INTEGER PRIMARY KEY,
    categoryId  INTEGER NOT NULL,
    title       TEXT    NOT NULL,
    author      TEXT    NOT NULL,
    isbn        TEXT    NOT NULL UNIQUE CHECK (length(isbn) = 13),
    publishYear INTEGER CHECK (publishYear BETWEEN 1800 AND 2100),
    price       REAL    NOT NULL CHECK (price > 0),
    image       TEXT    NOT NULL,
    readNow     INTEGER NOT NULL DEFAULT 0 CHECK (readNow IN (0, 1)),
    FOREIGN KEY (categoryId) REFERENCES category(categoryId)
);

CREATE INDEX idx_book_categoryId ON book(categoryId);
