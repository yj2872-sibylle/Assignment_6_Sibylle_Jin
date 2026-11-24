# Reel & Frame Books

**Name:** Sibylle Jin

## About the bookstore

Reel & Frame Books is a small bookstore for people who study or make media. It sells books in five categories: Film Criticism, Screenwriting, Filmmaking, Media Theory, and Photography. Each book has its title, author, ISBN, publication year, price, a cover image filename, and a `readNow` flag that marks the store's recommended reads.

## Files

| File | Purpose |
|---|---|
| `createTables.sql` | Creates the `category` and `book` tables with primary keys, a foreign key, and NOT NULL / UNIQUE / CHECK constraints |
| `insertRows.sql` | Inserts 5 categories and 15 real books (3 per category) |
| `bookstore.db` | The SQLite database built from the two SQL files |
| `bookstore_cli.py` | Command-line program for browsing and managing books |

## Create the database

From this folder, run:

```bash
sqlite3 bookstore.db < createTables.sql
sqlite3 bookstore.db < insertRows.sql
```

`createTables.sql` drops the tables first, so running both commands again resets the database to the sample data.

## Run the program

```bash
python3 bookstore_cli.py
```

Menu:

1. View all categories
2. View all books
3. View books in a category (JOIN of `book` and `category`)
4. Search books by title
5. Add a new book
6. Update a book price
7. Delete a book (asks for confirmation)
8. Search books by author (additional feature)
9. Find books in a price range (additional feature)
0. Quit

All queries that use user input are parameterized with `?` placeholders. The program turns on `PRAGMA foreign_keys = ON` for its connection, so a new book must belong to an existing category.
