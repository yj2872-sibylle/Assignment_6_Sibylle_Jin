"""
Reel & Frame Books - command-line interface
Author: Sibylle Jin

Connects to bookstore.db and lets the user browse and manage books.
Every query that uses user input is parameterized with ? placeholders.
"""

import sqlite3

DB_FILE = "bookstore.db"


# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------

def line() -> None:
    print("=" * 60)


def wait() -> None:
    input("\n(press Enter to return to the menu)")


def show_table(headers: list[str], rows: list[tuple]) -> None:
    """Print query results as a simple aligned table."""
    if not rows:
        print("Nothing found.")
        return
    # show prices (floats) with two decimals
    rows = [tuple(f"{v:.2f}" if isinstance(v, float) else v for v in row) for row in rows]
    widths = [len(h) for h in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))
    print("  ".join(h.ljust(widths[i]) for i, h in enumerate(headers)))
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print("  ".join(str(v).ljust(widths[i]) for i, v in enumerate(row)))


def ask_int(prompt: str) -> int | None:
    """Ask for a whole number; return None if the input is not one."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Please enter a whole number.")
        return None


def ask_price(prompt: str) -> float | None:
    """Ask for a price; return None if the input is not a number."""
    try:
        return round(float(input(prompt).strip()), 2)
    except ValueError:
        print("Please enter a number, for example 19.99.")
        return None


# ---------------------------------------------------------------
# READ
# ---------------------------------------------------------------

def list_categories(cur: sqlite3.Cursor) -> None:
    cur.execute("""
        SELECT categoryId, categoryName, categoryDescription, categoryImage
        FROM category
        ORDER BY categoryId
    """)
    show_table(["ID", "Category", "Description", "Image"], cur.fetchall())


def list_books(cur: sqlite3.Cursor) -> None:
    cur.execute("""
        SELECT bookId, title, author, price, readNow
        FROM book
        ORDER BY bookId
    """)
    show_table(["ID", "Title", "Author", "Price", "Read now"], cur.fetchall())


def books_in_category(cur: sqlite3.Cursor) -> None:
    list_categories(cur)
    category_id = ask_int("\nCategory ID: ")
    if category_id is None:
        return
    cur.execute("""
        SELECT b.bookId, b.title, b.author, b.price, c.categoryName
        FROM book AS b
        JOIN category AS c ON b.categoryId = c.categoryId
        WHERE c.categoryId = ?
        ORDER BY b.title
    """, (category_id,))
    show_table(["ID", "Title", "Author", "Price", "Category"], cur.fetchall())


def search_title(cur: sqlite3.Cursor) -> None:
    keyword = input("Title keyword: ").strip()
    cur.execute("""
        SELECT bookId, title, author, price
        FROM book
        WHERE title LIKE ?
        ORDER BY title
    """, (f"%{keyword}%",))
    show_table(["ID", "Title", "Author", "Price"], cur.fetchall())


# Additional feature 1: search by author
def search_author(cur: sqlite3.Cursor) -> None:
    keyword = input("Author name (or part of it): ").strip()
    cur.execute("""
        SELECT bookId, author, title, publishYear
        FROM book
        WHERE author LIKE ?
        ORDER BY author, title
    """, (f"%{keyword}%",))
    show_table(["ID", "Author", "Title", "Year"], cur.fetchall())


# Additional feature 2: books within a price range
def price_range(cur: sqlite3.Cursor) -> None:
    low = ask_price("Minimum price: ")
    high = ask_price("Maximum price: ")
    if low is None or high is None:
        return
    if low > high:
        low, high = high, low
    cur.execute("""
        SELECT b.bookId, b.title, c.categoryName, b.price
        FROM book AS b
        JOIN category AS c ON b.categoryId = c.categoryId
        WHERE b.price BETWEEN ? AND ?
        ORDER BY b.price
    """, (low, high))
    show_table(["ID", "Title", "Category", "Price"], cur.fetchall())


# ---------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------

def add_book(cur: sqlite3.Cursor) -> None:
    list_categories(cur)
    category_id = ask_int("\nCategory ID: ")
    if category_id is None:
        return
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    isbn = input("ISBN (13 digits): ").strip().replace("-", "")
    year = ask_int("Publication year: ")
    price = ask_price("Price: ")
    image = input("Image filename: ").strip()
    read_now = input("Mark as a 'read now' pick? (y/n): ").strip().lower() == "y"

    if not title or not author or year is None or price is None:
        print("Book not added: title, author, year and price are required.")
        return

    try:
        cur.execute("""
            INSERT INTO book (categoryId, title, author, isbn, publishYear,
                              price, image, readNow)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (category_id, title, author, isbn, year, price, image, int(read_now)))
        print(f"Added '{title}' with book ID {cur.lastrowid}.")
    except sqlite3.IntegrityError as err:
        # unknown category, duplicate or wrong-length ISBN, bad price or year
        print("Book not added:", err)


# ---------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------

def change_price(cur: sqlite3.Cursor) -> None:
    book_id = ask_int("Book ID: ")
    if book_id is None:
        return
    new_price = ask_price("New price: ")
    if new_price is None:
        return
    try:
        cur.execute("UPDATE book SET price = ? WHERE bookId = ?", (new_price, book_id))
    except sqlite3.IntegrityError as err:
        print("Price not changed:", err)
        return
    if cur.rowcount == 0:
        print(f"No book with ID {book_id}.")
    else:
        print(f"Book {book_id} now costs ${new_price:.2f}.")


# ---------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------

def remove_book(cur: sqlite3.Cursor) -> None:
    book_id = ask_int("Book ID to delete: ")
    if book_id is None:
        return
    cur.execute("SELECT title FROM book WHERE bookId = ?", (book_id,))
    row = cur.fetchone()
    if row is None:
        print(f"No book with ID {book_id}.")
        return
    if input(f"Delete '{row[0]}'? (y/n): ").strip().lower() != "y":
        print("Cancelled.")
        return
    cur.execute("DELETE FROM book WHERE bookId = ?", (book_id,))
    print("Book deleted.")


# ---------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------

MENU = [
    ("1", "View all categories", list_categories),
    ("2", "View all books", list_books),
    ("3", "View books in a category", books_in_category),
    ("4", "Search books by title", search_title),
    ("5", "Add a new book", add_book),
    ("6", "Update a book price", change_price),
    ("7", "Delete a book", remove_book),
    ("8", "Search books by author", search_author),
    ("9", "Find books in a price range", price_range),
]


def main() -> None:
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")   # off by default in each connection
    cur = conn.cursor()
    actions = {key: func for key, _, func in MENU}

    line()
    print("Welcome to Reel & Frame Books")
    print("Books on film, screenwriting, media and photography")

    try:
        while True:
            line()
            for key, label, _ in MENU:
                print(f" {key}. {label}")
            print(" 0. Quit")
            choice = input("\nChoose an option: ").strip()

            if choice == "0":
                print("Goodbye!")
                break
            if choice not in actions:
                print("Not a menu option, try again.")
                continue

            line()
            actions[choice](cur)
            conn.commit()      # save any insert, update or delete
            wait()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
