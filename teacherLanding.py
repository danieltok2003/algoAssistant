from tkinter import *
import sqlite3
from generatingSalt import generatePassword
import os
import sys

# TODO - report gives time in seconds, not minutes
file = sqlite3.connect(f'data.db')
f = file.cursor()

questionFile = 'questions'

minutes = 0


def secondsToMinutes(seconds):
    global minutes
    if seconds < 60:
        time = f'{minutes}.{str(round(seconds / 60, 1))[2:]}'   # [2:] to ignore 0
        minutes = 0  # clear for next session
        return time
    minutes += 1
    return secondsToMinutes(seconds - 60)


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
        except TypeError:  # if a class has no students but it has a teacher, ignore adding students to prevent NoneType string concatenation
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
    IDrange = []
    for item in f.fetchall():
        print(f'{item[0]} : {item[1]}')
        IDrange.append(item[0])

    ID = input('Enter ID of user/classroom to delete: ')  # TODO - check if ID exists
    if ID.isalpha() is True:
        print('Invalid input. Must be integer.')
        return 0
    if int(ID) not in IDrange:
        print('Invalid input. Input must be an existing ID')
        return 0
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
        if len(className) == 0:
            print('Class name cannot be blank')
            return 0
        f.execute("SELECT teacherID, userName, classID FROM Teachers")
        print("|  ID  |  NAME  |")
        IDrange = []
        for item in f.fetchall():
            print(f'{item[0]} : {item[1]}')
            IDrange.append(item[0])

        teacherID = input('Choose assigned teacher ID: ')
        if teacherID.isalpha() is True:
            print('Invalid input. Must be integer')
            return 0
        if int(teacherID) not in IDrange:
            print('Invalid ID. Try again')
            return 0

        ID = len(classRoomData) + 1
        f.execute("INSERT INTO Classrooms VALUES (?, ?, ?)", (ID, teacherID, className,))
    else:
        firstName = input('First name: ')
        lastName = input('Last name: ')
        password = input('Assign password: ')
        classID = input('Assign classID: ')  # TODO - VERIFY if classID exists

        if len(firstName) == 0 or len(lastName) == 0 or len(password) == 0 or len(classID) == 0:
            print('One of the entered fields is empty. Try again')
            return 0
        else:
            userName = firstName[0].lower() + firstName[1:].lower() + lastName[0].upper() + lastName[1:].lower()  # all usernames are camelcase names

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
    IDrange = []
    for item in f.fetchall():
        print(f'{item[0]} : {item[1]}')
        IDrange.append(item[0])

    ID = input('Give the ID of the desired student report: ')  # TODO - verification
    if ID.isalpha() is True:
        print('Invalid input. Must be integer.')
        return 0
    if int(ID) not in IDrange:
        print('Invalid ID entered. Try again')
        return 0
    f.execute("""
            SELECT userName, timeSpent, questionsAttempted, questionsCorrect
            FROM Students S
            WHERE S.studentID=?
              
              """, (int(ID),))
    report = list(f.fetchone())
    print(f'| Student {report[0]} Report |')
    print(f'{secondsToMinutes(report[1])} minutes spent')
    print(f'{report[2]} questions attempted')
    print(f'{report[3]} questions answered correctly')


def layoutQuestions():
    with open(questionFile, 'r') as questions:
        print('|qNum| Question|')
        for questionNumber, question in enumerate(questions.readlines()):  # gives numbered list of question num to Q
            print(f'{questionNumber}.  {question}')
        questions.close()


def addQuestion():
    question = input('Add question: ')
    if len(question) == 0:
        print('Question cannot be blank. Try again')
        return 0
    options = input('Add 4 comma separated options, with the first being the correct option: ')
    while options.count(',') != 3:
        print('Need exactly 4 options')
        options = input('Add 4 comma separated options, with the first being the correct option: ')

    with open(questionFile, 'a') as questions:
        questions.write(question + f' *{options}*' + '\n')
        questions.close()
    layoutQuestions()


def removeQuestion():
    with open(questionFile, 'r+') as questions:
        questionList = questions.readlines()
        print('|qNum| Question|')
        for questionNumber, question in enumerate(questionList):  # gives numbered list of question num to Q
            print(f'{questionNumber}.  {question}')

        while True:
            try:
                removeNum = int(input('Remove question number: '))
                break
            except ValueError:
                print('Must enter an integer')

        del questionList[removeNum]  # removes desired question from list
        questions.truncate(0)  # clears file to prep for readding rest of questions
        for line in questionList:
            questions.write(line)

    layoutQuestions()





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
    quiz questions
    """

    addQ = Button(root, text='Add question', command=addQuestion)
    addQ.pack()

    removeQ = Button(root, text='Remove question', command=removeQuestion)
    removeQ.pack()


    """
    main loop
    """
    root.mainloop()


if __name__ == '__main__':
    def refresh():
        root.destroy()
        main()
    main()