import sqlite3 as sq

MAJORS = ["undeclared",
          "computer science",
          "math",
          "physics",
          "biology",
          "chemistry",
          "psychology"]


def connect():
    # Connect to the database
    conn = sq.connect("studentdb.sqlite")
    # Create a cursor to the database
    curr = conn.cursor()

    return conn, curr

def create_table(curr):
    drop_first = """
    DROP TABLE IF EXISTS Student
    """
    curr.execute(drop_first)

    cmd = """
    CREATE TABLE Student(
    id INTEGER,
    name TEXT,
    email TEXT,
    major INTEGER
    );
    """
    curr.execute(cmd)


def add_information(conn,curr):
    cmd = """
    INSERT INTO Student(id, name, email, major)
    VALUES (10000000, 'Abby', 'abby@occ.edu', 1);
    """
    curr.execute(cmd)
    conn.commit()

    id = 10000001
    for i in range(5):
        name = input("Enter the name: ")
        email = name + "@occ.edu"
        major = input("Enter the major: ")

        try:
            major_id = MAJORS.index(major.lower())
        except ValueError:
            major_id = 0

        cmd = """
        INSERT INTO Student(id, name, email, major)
        VALUES(?, ?, ?, ?)
        """
        curr.execute(cmd, (id, name, email, major_id))
        conn.commit()
        id += 1

def pretty_print_table(records):
    print()
    print("{:12s}{:30s}{:30s}{:10s}".format("ID","Name", "Email","Major" ))

    for rec in records:
        print("{:<12d}{:30s}{:30s}{:10s}".format(rec[0],rec[1], rec[2], MAJORS[rec[3]]))

    print()


def see_all(curr):
    cmd = "SELECT * FROM Student ORDER BY major DESC"
    curr.execute(cmd)

    records = curr.fetchall()
    pretty_print_table(records)

def see_math_majors(curr):
    cmd = "SELECT name FROM Student WHERE major=2"
    curr.execute(cmd)
    records = curr.fetchall()

    print("Math Majors")
    for rec in records:
        print(rec[0])

def update_table(conn, curr):
    chem_id = MAJORS.index("chemistry")
    cmd = """
    UPDATE Student
    SET major=1
    WHERE major=?
    """
    curr.execute(cmd, (chem_id,))
    see_all(curr)
    conn.commit()

def delete_record(conn, curr):
    cmd = "DELETE FROM Student WHERE major=4"
    curr.execute(cmd)
    conn.commit()
    see_all(curr)

def main():
    # 1. Connect to the database
    conn, curr = connect()

    # 2. Create a table
    create_table(curr)

    # 3. Add data
    add_information(conn, curr)

    # 4. See information
    print("\n\n")
    see_all(curr)

    # 5. See math majors
    see_math_majors(curr)

    #6 Delete Records
    delete_record(conn, curr)

    # 7. Update chem to cs
    update_table(conn, curr)

    conn.close()

if __name__ == "__main__":
    main()