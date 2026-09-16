import sqlite3
from datetime import datetime


# =========================================================
# DATABASE
# =========================================================

DATABASE = "library.db"


def connect_db():
    return sqlite3.connect(DATABASE)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            quantity INTEGER NOT NULL,
            available INTEGER NOT NULL
        )
    """)

    # Members table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
    """)

    # Issue records
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issued_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# ADD BOOK
# =========================================================

def add_book():

    print("\n========== ADD BOOK ==========")

    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    category = input("Enter category: ").strip()

    try:
        quantity = int(input("Enter quantity: "))

        if quantity <= 0:
            print("❌ Quantity must be greater than 0.")
            return

    except ValueError:
        print("❌ Please enter a valid number.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO books
        (title, author, category, quantity, available)
        VALUES (?, ?, ?, ?, ?)
    """, (title, author, category, quantity, quantity))

    conn.commit()
    conn.close()

    print("\n✅ Book added successfully!")


# =========================================================
# VIEW ALL BOOKS
# =========================================================

def view_books():

    print("\n========== ALL BOOKS ==========")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, author, category, quantity, available
        FROM books
        ORDER BY id
    """)

    books = cursor.fetchall()

    conn.close()

    if not books:
        print("📚 No books found.")
        return

    print("-" * 90)

    print(
        f"{'ID':<5}"
        f"{'Title':<25}"
        f"{'Author':<20}"
        f"{'Category':<15}"
        f"{'Qty':<8}"
        f"{'Available':<10}"
    )

    print("-" * 90)

    for book in books:

        print(
            f"{book[0]:<5}"
            f"{book[1][:23]:<25}"
            f"{book[2][:18]:<20}"
            f"{book[3][:13]:<15}"
            f"{book[4]:<8}"
            f"{book[5]:<10}"
        )

    print("-" * 90)


# =========================================================
# SEARCH BOOK
# =========================================================

def search_book():

    print("\n========== SEARCH BOOK ==========")

    keyword = input(
        "Enter title, author or category: "
    ).strip()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, author, category, quantity, available
        FROM books
        WHERE title LIKE ?
        OR author LIKE ?
        OR category LIKE ?
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    books = cursor.fetchall()

    conn.close()

    if not books:
        print("❌ No matching books found.")
        return

    print()

    for book in books:

        print(f"ID        : {book[0]}")
        print(f"Title     : {book[1]}")
        print(f"Author    : {book[2]}")
        print(f"Category  : {book[3]}")
        print(f"Quantity  : {book[4]}")
        print(f"Available : {book[5]}")
        print("-" * 40)


# =========================================================
# REMOVE BOOK
# =========================================================

def remove_book():

    print("\n========== REMOVE BOOK ==========")

    try:
        book_id = int(input("Enter book ID: "))
    except ValueError:
        print("❌ Invalid ID.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT title FROM books WHERE id = ?",
        (book_id,)
    )

    book = cursor.fetchone()

    if not book:
        print("❌ Book not found.")
        conn.close()
        return

    cursor.execute(
        "DELETE FROM books WHERE id = ?",
        (book_id,)
    )

    conn.commit()
    conn.close()

    print(f"✅ '{book[0]}' removed successfully.")


# =========================================================
# ADD MEMBER
# =========================================================

def add_member():

    print("\n========== REGISTER MEMBER ==========")

    name = input("Enter member name: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone number: ").strip()

    if not name:
        print("❌ Member name cannot be empty.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO members
        (name, email, phone)
        VALUES (?, ?, ?)
    """, (name, email, phone))

    conn.commit()
    conn.close()

    print("\n✅ Member registered successfully!")


# =========================================================
# VIEW MEMBERS
# =========================================================

def view_members():

    print("\n========== MEMBERS ==========")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, phone
        FROM members
        ORDER BY id
    """)

    members = cursor.fetchall()

    conn.close()

    if not members:
        print("❌ No members registered.")
        return

    print("-" * 75)

    print(
        f"{'ID':<5}"
        f"{'Name':<25}"
        f"{'Email':<25}"
        f"{'Phone':<15}"
    )

    print("-" * 75)

    for member in members:

        print(
            f"{member[0]:<5}"
            f"{member[1][:23]:<25}"
            f"{member[2][:23]:<25}"
            f"{member[3]:<15}"
        )

    print("-" * 75)


# =========================================================
# ISSUE BOOK
# =========================================================

def issue_book():

    print("\n========== ISSUE BOOK ==========")

    try:
        book_id = int(input("Enter book ID: "))
        member_id = int(input("Enter member ID: "))
    except ValueError:
        print("❌ Please enter valid IDs.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Check book
    cursor.execute("""
        SELECT title, available
        FROM books
        WHERE id = ?
    """, (book_id,))

    book = cursor.fetchone()

    if not book:
        print("❌ Book not found.")
        conn.close()
        return

    if book[1] <= 0:
        print("❌ Book is currently unavailable.")
        conn.close()
        return

    # Check member
    cursor.execute("""
        SELECT name
        FROM members
        WHERE id = ?
    """, (member_id,))

    member = cursor.fetchone()

    if not member:
        print("❌ Member not found.")
        conn.close()
        return

    # Check if already issued
    cursor.execute("""
        SELECT id
        FROM issued_books
        WHERE book_id = ?
        AND member_id = ?
        AND status = 'Issued'
    """, (book_id, member_id))

    existing = cursor.fetchone()

    if existing:
        print("❌ This member already has this book.")
        conn.close()
        return

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO issued_books
        (book_id, member_id, issue_date, status)
        VALUES (?, ?, ?, ?)
    """, (
        book_id,
        member_id,
        today,
        "Issued"
    ))

    cursor.execute("""
        UPDATE books
        SET available = available - 1
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    conn.close()

    print("\n✅ Book issued successfully!")
    print(f"📖 Book   : {book[0]}")
    print(f"👤 Member : {member[0]}")
    print(f"📅 Date   : {today}")


# =========================================================
# RETURN BOOK
# =========================================================

def return_book():

    print("\n========== RETURN BOOK ==========")

    try:
        book_id = int(input("Enter book ID: "))
        member_id = int(input("Enter member ID: "))
    except ValueError:
        print("❌ Please enter valid IDs.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, issue_date
        FROM issued_books
        WHERE book_id = ?
        AND member_id = ?
        AND status = 'Issued'
    """, (book_id, member_id))

    record = cursor.fetchone()

    if not record:
        print("❌ No active issue record found.")
        conn.close()
        return

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        UPDATE issued_books
        SET return_date = ?,
            status = 'Returned'
        WHERE id = ?
    """, (today, record[0]))

    cursor.execute("""
        UPDATE books
        SET available = available + 1
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    conn.close()

    print("\n✅ Book returned successfully!")
    print(f"📅 Return date: {today}")


# =========================================================
# ISSUED BOOKS
# =========================================================

def view_issued_books():

    print("\n========== ISSUED BOOKS ==========")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            issued_books.id,
            books.title,
            members.name,
            issued_books.issue_date,
            issued_books.return_date,
            issued_books.status
        FROM issued_books

        JOIN books
        ON issued_books.book_id = books.id

        JOIN members
        ON issued_books.member_id = members.id

        ORDER BY issued_books.id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    if not records:
        print("📚 No issue records found.")
        return

    for record in records:

        print("-" * 60)

        print(f"Record ID   : {record[0]}")
        print(f"Book        : {record[1]}")
        print(f"Member      : {record[2]}")
        print(f"Issue Date  : {record[3]}")
        print(f"Return Date : {record[4] or 'Not returned'}")
        print(f"Status      : {record[5]}")

    print("-" * 60)


# =========================================================
# STATISTICS
# =========================================================

def statistics():

    print("\n========== LIBRARY STATISTICS ==========")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM books"
    )

    total_book_types = cursor.fetchone()[0]

    cursor.execute(
        "SELECT SUM(quantity) FROM books"
    )

    total_books = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT SUM(available) FROM books"
    )

    available_books = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT COUNT(*) FROM members"
    )

    total_members = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM issued_books
        WHERE status = 'Issued'
    """)

    issued_books = cursor.fetchone()[0]

    conn.close()

    print(f"📚 Book Types     : {total_book_types}")
    print(f"📖 Total Books    : {total_books}")
    print(f"✅ Available Books: {available_books}")
    print(f"📤 Issued Books   : {issued_books}")
    print(f"👥 Members        : {total_members}")


# =========================================================
# MAIN MENU
# =========================================================

def main():

    create_tables()

    while True:

        print("\n")
        print("=" * 50)
        print("       📚 LIBRARY MANAGEMENT SYSTEM")
        print("=" * 50)

        print("""
1. 📖 Add Book
2. 📚 View All Books
3. 🔍 Search Book
4. 🗑️ Remove Book

5. 👤 Register Member
6. 👥 View Members

7. 📤 Issue Book
8. 📥 Return Book
9. 📋 View Issue Records

10. 📊 Library Statistics

0. 🚪 Exit
""")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            add_book()

        elif choice == "2":
            view_books()

        elif choice == "3":
            search_book()

        elif choice == "4":
            remove_book()

        elif choice == "5":
            add_member()

        elif choice == "6":
            view_members()

        elif choice == "7":
            issue_book()

        elif choice == "8":
            return_book()

        elif choice == "9":
            view_issued_books()

        elif choice == "10":
            statistics()

        elif choice == "0":

            print("\n👋 Thank you for using the Library Management System!")

            break

        else:

            print("\n❌ Invalid choice. Please try again.")


# =========================================================
# RUN PROGRAM
# =========================================================

if __name__ == "__main__":
    main()