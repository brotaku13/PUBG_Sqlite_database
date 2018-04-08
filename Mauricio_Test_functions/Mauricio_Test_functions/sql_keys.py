# sqlitebrowser
# sqlite3 shell (.tables to see tables; .schema echoes CREATE)

import sqlite3 as sq

# Setting Primary Keys
#      Autoincrement
#      Unique
#      Not Null
#      Set starting value??


# Using Foreign Keys


# Setting up Multiple Tables
#    Student, Instructor, Course
# Does an instructor belong to a course, or a course to an instructor?
# Each course can only have one instructor


# Many to Many
#  One Student can take many courses

MAJORS = ["undeclared", 
          "computer science", 
          "math", 
          "physics", 
          "biology",
          "chemistry", 
          "psychology"]


def connect(fname):
    conn = sq.connect(fname)
    cur = conn.cursor()

    return conn, cur

def cleandb(cur, tables):
    cmd = "DROP TABLE IF EXISTS {}"
    for table in tables:
        drop = cmd.format(table)
        cur.execute(drop)

def add_students(cur):
    insert = """INSERT INTO Student(name, major) VALUES(?, ?)"""
    for i in range(5):
        name = input("Enter student name: ")
        
        while True:
            major = input("Enter student major: ")
            major = major.lower().strip()
            if major in MAJORS:
                major_id = MAJORS.index(major)
                break
            print("Not a valid major")
        
        cur.execute(insert, (name, major_id))
    
def add_instructors(cur):

    cmd = """
    INSERT INTO Instructor(first_name, last_name)
    VALUES ("KATHRYN", "RODGERS"),
    ("GABRIELA", "ERNSBERGER"),
    ("STEVE", "GILBERT"),
    ("BILL","SAICHEK"),
    ("MICHAEL","PAULDING");
    """
    
    cur.execute(cmd)


def add_courses(cur):
    # ask for  coursename
    # who teaches?
    
    for i in range(5):
        course = input("Enter course name: ")
        prof = input("Who teaches it? ").strip().upper()
        time = input("What time? (HH:SS) ")
        
        cmd = """
        INSERT INTO Course(name, instructor_id, time)
        VALUES (?, ?, time(?))
        """
        
        # Get the prof ID
        get_prof = """SELECT id FROM Instructor WHERE first_name=? AND last_name=?"""
        print(prof.split())
        cur.execute(get_prof, tuple(prof.split()))
        
        prof_id = cur.fetchone()[0]
        
        # Add Course
        cur.execute(cmd, (course, prof_id, time))
    


def enroll_students_by_id(cur):
    student_id = input("Enter student id: ")
    course_id = input("Enter course id: ")
    
    try:
        cmd = """
        INSERT OR IGNORE INTO Enrollment(student_id, course_id)
        VALUES (?, ?)
        """
        cur.execute(cmd, (student_id, course_id))
        
    except Exception as e:
        print(e)


def enroll_students_by_name(cur):
    student_name = input("Enter student's full name: ").strip()
    course_name = input("Enter course name: ").strip()
    time = input("Enter time of course (HH:SS): ").strip()


    try:
        cmd = """
        INSERT OR IGNORE INTO Enrollment(student_id, course_id)
        VALUES (
        (SELECT id FROM Student WHERE name=?),
        (SELECT id FROM Course WHERE name=? AND time=time(?))
        );
        """
        cur.execute(cmd, (student_name, course_name, time));
    except Exception as e:
        print(e)
    
def main():
    ### Primary Keys
    try:
        tables = ["Student", "Instructor", "Course", "Enrollment"]
        # Connect to database
        print("\nConnecting to database....\n")
        conn,cur = connect("schooldb.sqlite")
        
        # Clean out the database
        cleandb(cur, tables)
    
        # Create Student Table
        # Create Instructor Table
      
        create_tables = """CREATE TABLE Student(
        id INTEGER PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        major INTEGER
        );
        
        CREATE TABLE Instructor(
        id INTEGER PRIMARY KEY NOT NULL,
        first_name TEXT,
        last_name TEXT
        );       
        """

        print("\nCreating Tables\n")
        cur.executescript(create_tables)
        conn.commit()
        
        # Add Students/Instructors/Courses
        # PRIMARY KEY means if you don't supply an id, one will be provided
        # To set the starting value, add the first value with an id
        print("\n\nAdding Students\n\n")
        
        add_students(cur)
        print("\n\nAdding Instructors\n\n")
        add_instructors(cur)
        
        conn.commit()
        ####################
        ## sqlite shell
        # .tables to see the tables
        # .schema to see creates
        # SELECT * FROM Table; to see everything

        ####################
        ## Foreign Keys
        # Course belong to an instructor or instructor belong to a course?
        ## Time Field (TEXT with time() function)
        # Actually, we would probably want another table Location
        # Create Course Table
        create_course_table = """
        CREATE TABLE Course(
        id INTEGER PRIMARY KEY NOT NULL,
        instructor_id INTEGER NOT NULL,
        name TEXT,
        time TEXT
        );
        """
        print("\n\nCreate Course Table\n\n")
        cur.execute(create_course_table)
        print("\n\nAdding Courses\n\n")
        add_courses(cur)
        conn.commit()
        #######################
        ## Print out which courses each instructor teaches

        cmd = """
        SELECT name FROM Course WHERE instructor_id = (SELECT id FROM Instructor WHERE last_name="RODGERS");
        """
        cur.execute(cmd)
        res = cur.fetchall()
        print(res)
        
        ##############################
        ## Many to Many Relationship
        # Create Enrollment Table
        create_enroll = """
        CREATE TABLE Enrollment(
        student_id INTEGER,
        course_id INTEGER,
        PRIMARY KEY(student_id, course_id)
        );
        """
        cur.execute(create_enroll)

        print("\n\nEnrolling by ID\n\n")
        enroll_students_by_id(cur)
        print("\n\nEnrolling by Name\n\n")
        enroll_students_by_name(cur)
        
        ###########################
        ## Print out what courses have people enrolled
        cmd = """
        SELECT name FROM Course 
        WHERE id IN (SELECT course_id FROM Enrollment);
        """
        cur.execute(cmd)
        res = cur.fetchall()
        print("\nThese courses have people enrolled: ")
        for course in res:
            print(course[0])

    except Exception as e:
        print(e)
        
    finally:
        conn.close()



if __name__ == "__main__":
    main()
