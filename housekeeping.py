import sqlite3


def wipeDataBaseFiles():
    with open('data.db', 'w') as file:
        file.write('')


def clearRecords():
    file = sqlite3.connect(f'data.db')
    f = file.cursor()
    f.execute("DELETE FROM Teachers WHERE userName != 'joeBloggs'")
    file.commit()
    print('wiped')



wipeDataBaseFiles()
# clearRecords()