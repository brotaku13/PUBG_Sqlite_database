# Here's a pretty good reference: https://www.w3schools.com/sql/default.asp
# Keep in mind, there are different flavors of SQL
# Some things only work with regular SQL, some with SQLite,etc

import sqlite3 as sq

def connect(fname):
    conn = sq.connect(fname)
    cur = conn.cursor()

    return conn, cur


def create_book_table(cur):
    """ Create table, dropping first if needed """
    cmd = """
    DROP TABLE IF EXISTS Book;
    CREATE TABLE Book(
    barcode INTEGER,
    title TEXT,
    author TEXT
    );
    """
    # executescript -- allows for multiple SQL statements in the string
    cur.executescript(cmd)

def create_patron_table(cur):
    """ Create table, dropping first if needed """
    cmd = """
    DROP TABLE IF EXISTS Patron;
    CREATE TABLE Patron(
    card_number INTEGER,
    name TEXT,
    zipcode INTEGER
    );
    """
    # executescript -- allows for multiple SQL statements in the string
    cur.executescript(cmd)


def print_table(records, column_headers):
    """Pretty print the records with given column headers"""
    # Create a format string making each column left aligned and 30 characters wide
    fmt_string = "{:<30}" * len(column_headers)

    # Print header row
    print(fmt_string.format(*column_headers))

    # Print records
    # records is a list of tuples
    # each tuple is a specific record in the database
    # *row expands the tuple into separate arguments for format
    for row in records:
        print(fmt_string.format(*row))
    
    
def add_books(cur):
    """Add books to the table Books"""
    # Hardcoded so this code will run for you
    # You can actually add multiple rows at a time
    cmd = """
    INSERT INTO Book(barcode, title, author)
    VALUES (1111111,"The Lies of Locke Lamora", "Scott Lynch"),
    (1111112, "Mostly Harmless", "Douglas Adams"),
    (1111113, "The Alchemyst",  "Michael Scott"),
    (1111114, "New Spring", "Robert Jordan" ),
    (1111115, "The Lost Gate", "Orson Scott Card");
    """
    cur.execute(cmd)
    

def add_patrons(cur):
    """Add patrons to the table Patrons"""
    # Hardcoded so this code will run for you
    cmd = """
    INSERT INTO Patron(card_number, name, zipcode)
    VALUES (123456789, "Tyler Sorensen", 93553),
    (123456781, "Leif Andersen", 92626),
    (123456782, "Chad Brubaker",  84414),
    (123456783, "Brenden Tyler", 84412),
    (123456784, "Kevin Malby", 92616)
    """
    cur.execute(cmd)
    
    
def main():
    try:
        # Connect to the database
        conn,cur = connect("booksdb.sqlite")
        
        # Create the tables
        print("Creating tables....")
        create_book_table(cur)
        create_patron_table(cur)
        
        # Add records
        print("Adding records.....")
        add_books(cur)
        conn.commit()
        add_patrons(cur)
        conn.commit()

        # Pretty Print Book Table
        print("\nAll the Books\n")
        cur.execute("SELECT * FROM Book;")
        records = cur.fetchall()
        print_table(records, ["Barcode", "Title", "Author"])
        
        # Pretty print Patron table
        print("\nAll the Patrons\n")
        cur.execute("SELECT * FROM Patron;")
        records = cur.fetchall()
        print_table(records, ["Card Number", "Name", "Zipcode"])
        
        # Print out all zip codes
        print("\nAll of the zip codes\n")
        cur.execute("SELECT zipcode FROM Patron;")
        records = cur.fetchall()
        print_table(records, ["Zipcodes"])
        
        # Print out book table, ordered by author
        print("\nBooks ordered by author\n")
        cmd = """
        SELECT * FROM Book
        ORDER BY author
        """
        cur.execute(cmd)
        records = cur.fetchall()
        print_table(records, ["Barcode", "Title", "Author"])
        
        # print out all books' title and author
        print("\nBooks' title and author\n")
        cur.execute("SELECT title, author FROM Book")
        records = cur.fetchall()
        print_table(records, ["Title", "Author"])
        
        
        # Delete the third book in the table
        # This line will depend on what your third book was
        # Your delete will probably contain the specific information from that row
        # Here's a way to delete the third row without knowing what it contains
        print("\nDeleting third row\n")
        cmd = "DELETE FROM Book WHERE ROWID = 3"
        cur.execute(cmd)

        # Print the table to verify record was deleted
        cur.execute("SELECT * FROM Book;")
        records = cur.fetchall()
        print_table(records, ["Barcode", "Title", "Author"])
        
        # Add The Giver Blue by Lois Lowry
        # Don't forget put quotes around the strings in VALUES
        print("\nAdding The Giver Blue\n")
        cmd = """
        INSERT INTO Book(barcode, title, author)
        VALUES (3331642, "The Giver Blue", "Lois Lowry");
        """
        cur.execute(cmd)
        
        # Verify it was added
        cur.execute("SELECT * FROM Book;")
        records = cur.fetchall()
        print_table(records, ["Barcode", "Title", "Author"])

        # Update The Giver Blue to Gathering Blue
        # You technically can use the title or author to filter which row to update
        # I chose barcode because that's the primary key - it's purpose is to
        # uniquely identify the book
        print("\nUpdating title to the correct title\n")
        cmd = """
        UPDATE Book
        SET title="Gathering Blue"
        WHERE barcode=3331642
        """
        cur.execute(cmd)

        # Verify it was added
        cur.execute("SELECT * FROM Book;")
        records = cur.fetchall()
        print_table(records, ["Barcode", "Title", "Author"])
        
        
    except Exception as e:
        print(e)

    finally:
        # Save the changes
        conn.commit()
        # CLOSE THE DATABASE
        conn.close()
