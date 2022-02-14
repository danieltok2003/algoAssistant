import sqlite3
import hashlib
import os
import studentLanding
import teacherLanding
from tkinter import *

database = 'data.db'  # allow to be set by user

passingUser = ''

TeacherORStudent = ''

errorTypeToErrorMessage = {
    'invalidInput': 'Invalid input. Try again.',
    'invalidUser': 'Invalid username. Try again.',
    'invalidPassword': 'Invalid password. Try again.',
}


def checkUserType(userType):
    valid = False
    if userType == 'T' or userType == 'S':
        valid = True
    else:
        errorMessage('invalidInput')
    return valid


def grabUsernameListFromUserType(userType, f):
    if userType == 'teacher':
        f.execute("SELECT userName FROM Teachers")
    elif userType == 'student':
        f.execute("SELECT userName FROM Students")
    rows = f.fetchall()
    result = [i[0] for i in rows]  # converting tuple form to list form
    return result


def grabHashPassword(userType, userName, f):
    if userType == 'teacher':
        f.execute("SELECT hashPass FROM Teachers WHERE userName=?", (userName,))
    elif userType == 'student':
        f.execute("SELECT hashPass from Students WHERE userName=?", (userName,))
    hash = f.fetchone()[0]
    return hash


def authenticateUser(userType, userName, newPassword, auth):
    file = sqlite3.connect(database)
    f = file.cursor()
    """
    
    STAGE 1 - checking if username is valid
    
    """
    userList = grabUsernameListFromUserType(userType, f)
    if userName in userList:
        print('Username valid. Checking password... ')
    else:
        errorMessage('invalidUser')
        return auth

    """

    STAGE 2 - checking if password is valid

    """

    storage = grabHashPassword(userType, userName, f)
    storedSalt = storage[:32]
    storedKey = storage[32:]
    # saltFromStorage = hash[:32]
    # keyFromStorage = hash[32:]

    newKey = hashlib.pbkdf2_hmac(
        'sha256',
        newPassword.encode('utf-8'),
        storedSalt,  # apply stored salt to the new password
        100000,
        dklen=128
    )
    if newKey == storedKey:
        print('Password correct')
        auth = True
    else:
        errorMessage('invalidPassword')
    return auth


def errorMessage(errorType):
    print(errorTypeToErrorMessage[errorType])


def login():
    global TeacherORStudent
    userName = ''
    global passingUser
    stage1 = False  # stage 1 - checking user type
    stage2 = False  # stage 2 - authenticating user
    while stage1 is False or stage2 is False:  # main loop for authentication
        """
    
        STAGE 1 - checking if teacher or student
    
        """

        TeacherORStudent = input('Are you a teacher (T) or student (S)?: ')

        if checkUserType(TeacherORStudent) is False:  # fail test if input not T or S
            continue  # repeat while loop from top in fail case
        stage1 = True

        """

        STAGE 2 - verifying username and password

        """

        userName = input('Give username: ')
        password = input('Give password: ')

        auth = False
        if TeacherORStudent == 'T':
            auth = authenticateUser('teacher', userName, password, auth)
        elif TeacherORStudent == 'S':
            auth = authenticateUser('student', userName, password, auth)

        if auth is False:
            continue

        stage2 = True

    passingUser = userName

    print('User authenticated.')


if __name__ == '__main__':
    login()
    if TeacherORStudent == 'T':
        teacherLanding.main()
    else:
        studentLanding.main(passingUser)










