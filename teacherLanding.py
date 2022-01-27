from tkinter import *
import sqlite3
from generatingSalt import generatePassword
import os
import sys

file = sqlite3.connect(f'data.db')
f = file.cursor()


def relationShips():
    relation = ''

    for teacher in teacherData:
        try:
            userName = f'{teacher[0][0].lower()}{teacher[0][1:]}{teacher[1][0].upper()}{teacher[1][1:]}'

            relation += f'{teacher[0]} {teacher[1]} teaches Class '   # firstName lastName
            f.execute("""
            SELECT C.className 
            FROM Teachers T INNER JOIN Classrooms C
            ON T.classID = C.classID
            WHERE T.userName=?
            """, (userName,))  #  formatting User Name to userName

            relation += f.fetchone()[0]

            f.execute("""
            SELECT S.firstName, S.lastName
            FROM Teachers T INNER JOIN Students S
            ON T.classID = S.classID
            WHERE T.userName=?
            """, (userName,))

            relation += f' | {", ".join([" ".join(person) for person in f.fetchall()])} |'
            relation += '\n'
        except TypeError:
            continue

    return relation


def grabData(tableType):

    if tableType == 'teacher':
        f.execute("SELECT firstName, lastName FROM Teachers")
    elif tableType == 'student':
        f.execute("SELECT firstName, lastName FROM Students")
    elif tableType == 'classroom':
        f.execute("SELECT className FROM Classrooms")

    rows = f.fetchall()
    return rows


def removeRecord(tableType):   # TODO - verify not deleting classrooms with students/teachers assigned to them
    if tableType == 'teacher':
        f.execute("SELECT teacherID, userName FROM Teachers")
    elif tableType == 'student':
        f.execute("SELECT studentID, userName FROM Students")
    elif tableType == 'classroom':
        f.execute("SELECT classID, className FROM Classrooms")
    print("|  ID  |  NAME  |")
    for item in f.fetchall():
        print(f'{item[0]} : {item[1]}')

    ID = input('Enter ID of user/classroom to delete: ')  # TODO - check if ID exists
    if tableType == 'teacher':
        f.execute("DELETE FROM Teachers WHERE teacherID=?", (ID,))  # todo - unnecessary if repetition
    elif tableType == 'student':
        f.execute("DELETE FROM Students WHERE studentID=?", (ID,))
    elif tableType == 'classroom':
        f.execute("DELETE FROM Classrooms WHERE classID=?", (ID,))


    file.commit()
    print('Successful removal.')
    refresh()



"""

query list of class names, teacher names, student names

then at bottom, show teacher-class , list of students
add button to query student report
"""


def addData(tableType):
    if tableType == 'classroom':
        className = input('Class name: ')

        f.execute("SELECT teacherID, userName FROM Teachers")
        print("|  ID  |  NAME  |")
        for item in f.fetchall():
            print(f'{item[0]} : {item[1]}')

        teacherID = input('Choose assigned teacher ID: ')
        ID = len(classRoomData) + 1
        f.execute("INSERT INTO Classrooms VALUES (?, ?, ?)", (ID, teacherID, className,))
    else:
        firstName = input('First name: ')
        lastName = input('Last name: ')
        password = input('Assign password: ')
        classID = input('Assign classID: ')  # TODO - VERIFY if classID exists

        userName = firstName[0].lower() + firstName[1:] + lastName[0].upper() + lastName[1:]  # all usernames are camelcase names

        if tableType == 'teacher':
            ID = len(teacherData) + 1
            f.execute("INSERT INTO Teachers VALUES (?, ?, ?, ?, ?, ?)", (ID, classID, firstName, lastName, userName, generatePassword(password)))
        else:
            ID = len(studentData) + 1
            f.execute("INSERT INTO Students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (ID, classID, firstName, lastName, userName, generatePassword(password), 0, 0, 0))  # inserting 0s for 0 time spent, qAs, qCs

    file.commit()
    print(f'Success. User/classroom added.')
    refresh()  # restart window to show updates


def getReport():
    f.execute("SELECT studentID, userName FROM Students")
    print("|  ID  |  NAME  |")
    for item in f.fetchall():
        print(f'{item[0]} : {item[1]}')

    ID = int(input('Give the ID of the desired student report: '))  # TODO - verification

    f.execute("""
            SELECT userName, timeSpent, questionsAttempted, questionsCorrect
            FROM Students S
            WHERE S.studentID=?
              
              """, (ID,))
    report = list(f.fetchone())
    print(report)
    print(f'| Student {report[0]} Report |')
    print(f'{report[1]} minutes spent')
    print(f'{report[2]} questions attempted')
    print(f'{report[3]} questions answered correctly')


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

    extractReport = Button(root, text='Extract report', command=getReport)
    extractReport.pack()

    removeStudent = Button(root, text='Remove student', command=lambda: removeRecord('student'))
    removeStudent.pack()


    """
    classroom table
    """
    classroomLabel = Label(root, text='Classroom data:')
    classroomLabel.pack()
    classroomTable = Label(root, text=str(classRoomData), bg='white')
    classroomTable.pack()

    addClassroom = Button(root, text='Add classroom', command=lambda: addData('classroom'))
    addClassroom.pack()

    removeClassroom = Button(root, text='Remove classroom', command=lambda: removeRecord('classroom'))
    removeClassroom.pack()


    """
    relationship 
    """

    relateLabel = Label(root, text=relationShips(), bg='white')
    relateLabel.pack()


    """
    main loop
    """
    root.mainloop()


if __name__ == '__main__':
    def refresh():
        root.destroy()
        main()
    main()