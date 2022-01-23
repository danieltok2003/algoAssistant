import sqlite3


def wipeDataBaseFiles():
    with open('student.db', 'w') as file:
        file.write('')

    with open('teacher.db', 'w') as file:
        file.write('')

    with open('classroom.db', 'w') as file:
        file.write('')


def clearRecords(dbName):
    file = sqlite3.connect(f'{dbName}.db')
    f = file.cursor()
    f.execute("DELETE FROM Teachers WHERE userName != 'joeBloggs'")
    file.commit()
    print('wiped')

wipeDataBaseFiles()
# clearRecords('teacher')