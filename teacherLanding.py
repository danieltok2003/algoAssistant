from tkinter import *
import sqlite3
from generatingSalt import generatePassword
import os
import sys


def grabData(tableType):
    file = sqlite3.connect(f'{tableType}.db')
    f = file.cursor()
    if tableType == 'teacher':
        f.execute("""
        SELECT T.classID, T.firstName, T.lastName, S.firstName, S.classID
        FROM Teachers T INNER JOIN Students S
        ON T.classID = S.classID
        
        """)
    elif tableType == 'student':
        f.execute("SELECT userName, classID FROM Students")
    elif tableType == 'classroom':
        f.execute("SELECT className, teacherID FROM Classrooms")

    rows = f.fetchall()
    return rows


def removeRecord(tableType):   # TODO - verify not deleting classrooms with students/teachers assigned to them
    file = sqlite3.connect(f'{tableType}.db')
    f = file.cursor()
    if tableType == 'teacher':
        f.execute("SELECT teacherID, userName FROM Teachers")
    elif tableType == 'student':
        f.execute("SELECT studentID, userName FROM Students")
    elif tableType == 'classroom':
        f.execute("SELECT classID, className FROM Classrooms")
    print("|  ID  |  NAME  |")
    for item in f.fetchall():
        print(f'{item[0]}. {item[1]}')

    ID = input('Enter ID of user to delete: ')  # TODO - check if ID exists
    if tableType == 'teacher':
        f.execute("DELETE FROM Teachers WHERE teacherID=?", (ID,))  # todo - unnecessary if repetition
    elif tableType == 'student':
        f.execute("DELETE FROM Students WHERE studentID=?", (ID,))
    elif tableType == 'classroom':
        f.execute("DELETE FROM Classrooms WHERE classID=?", (ID,))

    file.commit()
    refresh()


def addData(tableType):
    file = sqlite3.connect(f'{tableType}.db')
    f = file.cursor()
    if tableType == 'classroom':
        pass
    else:
        firstName = input('First name: ')
        lastName = input('Last name: ')  # todo - VERIFY ONLY ALPHA CHARS
        password = input('Assign password: ')
        classID = input('Assign classID: ')  # TODO - VERIFY if classID exists

        userName = firstName[0].lower() + firstName[1:] + lastName[0].upper() + lastName[1:]  # all usernames are camelcase names

        if tableType == 'teacher':
            ID = len(teacherData) + 1
            f.execute("INSERT INTO Teachers VALUES (?, ?, ?, ?, ?, ?)", (ID, classID, firstName, lastName, userName, generatePassword(password)))
        else:
            ID = len(studentData) + 1
            f.execute("INSERT INTO Students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (ID, classID, firstName, lastName, userName, 0, 0, 0, generatePassword(password)))  # inserting 0s for 0 time spent, qAs, qCs
        print('Success. User added.')
        file.commit()
        refresh()  # restart window to show updates


def main():
    global root
    global teacherData
    global studentData
    global classRoomData

    teacherData = grabData('teacher')
    studentData = grabData('student')
    classRoomData = grabData('classroom')
    root = Tk()
    """
    page title
    """
    root.title(f'Teacher page')

    title = Label(root, text='Teacher page', font=('Arial', 16, 'bold'))
    title.pack()

    """
    teacher table
    """

    teacherLabel = Label(root, text='Teacher data:')
    teacherLabel.pack()
    teacherTable = Label(root, text=str(teacherData), bg='white')
    teacherTable.pack()

    addTeacher = Button(root, text='Add teacher', command=lambda: addData('teacher'))
    addTeacher.pack()

    removeTeacher = Button(root, text='Remove teacher', command=lambda: removeRecord('teacher'))
    removeTeacher.pack()


    """
    student table
    """

    studentLabel = Label(root, text='Student data:')
    studentLabel.pack()
    studentTable = Label(root, text=str(studentData), bg='white')
    studentTable.pack()

    addStudent = Button(root, text='Add student', command=lambda: addData('student'))
    addStudent.pack()


    """
    classroom table
    """
    classroomLabel = Label(root, text='Classroom data:')
    classroomLabel.pack()
    classroomTable = Label(root, text=str(classRoomData), bg='white')
    classroomTable.pack()

    """
    main loop
    """
    root.mainloop()


if __name__ == '__main__':
    def refresh():
        root.destroy()
        main()
    main()