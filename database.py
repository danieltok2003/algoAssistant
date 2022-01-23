import sqlite3

student = sqlite3.connect('student.db')
classroom = sqlite3.connect('classroom.db')
teacher = sqlite3.connect('teacher.db')


s = student.cursor()  # create student table /////////////////

s.execute("""
        CREATE TABLE Students (
            studentID INTEGER PRIMARY KEY,
            classID INTEGER,
            firstName TEXT,
            lastName TEXT,
            userName TEXT,
            hashPass TEXT,
            timeSpent REAL,
            questionsAttempted INTEGER,
            questionsCorrect INTEGER,
            FOREIGN KEY(classID) REFERENCES Classroom(classID)
)""")


c = classroom.cursor()  # creating classroom table //////////////

c.execute(
    """CREATE TABLE Classrooms (
            classID INTEGER PRIMARY KEY,
            teacherID INTEGER,
            className TEXT,
            FOREIGN KEY(teacherID) REFERENCES Teacher(teacherID)
            )"""
)


t = teacher.cursor()  # creating teacher table //////////////

t.execute(
    """CREATE TABLE Teachers (
            teacherID INTEGER PRIMARY KEY,
            classID INTEGER,
            firstName TEXT,
            lastName TEXT,
            userName TEXT,
            hashPass TEXT,
            FOREIGN KEY(classID) REFERENCES Classroom(classID)
            )"""
)


# commit command
student.commit()
classroom.commit()
teacher.commit()


# close connection
student.close()
classroom.close()
teacher.close()



# datatypes:
# NULL
# INTEGER
# REAL
# TEXT
# BLOB
