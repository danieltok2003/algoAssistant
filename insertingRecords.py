import sqlite3

student = sqlite3.connect('student.db')
classroom = sqlite3.connect('classroom.db')
teacher = sqlite3.connect('teacher.db')

#
# c.execute("""
#
#         INSERT INTO students VALUES ('joe', 'bloggs', 'joeb@gmail.com')
#
#
# """)