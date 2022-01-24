import sqlite3

data = sqlite3.connect('data.db')

d = data.cursor()

d.execute("""
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
            )
        """)

data.commit()

d.execute("""
    
        CREATE TABLE Classrooms (
            classID INTEGER PRIMARY KEY,
            teacherID INTEGER,
            className TEXT,
            FOREIGN KEY(teacherID) REFERENCES Teacher(teacherID)
            )
        """)

data.commit()

d.execute("""



 CREATE TABLE Teachers (
            teacherID INTEGER PRIMARY KEY,
            classID INTEGER,
            firstName TEXT,
            lastName TEXT,
            userName TEXT,
            hashPass TEXT,
            FOREIGN KEY(classID) REFERENCES Classroom(classID)
            )
            """)

# commit command
data.commit()

# close connection
data.close()



