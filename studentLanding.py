import login
from tkinter import *
import pathfinding
import sorting
import sqlite3
import os

file = sqlite3.connect(f'data.db')
f = file.cursor()
quizStats = 'studentSession'


def getStudentStats(userName):
    f.execute("""
        SELECT timeSpent, questionsAttempted, questionsCorrect
            FROM Students S
            WHERE S.userName=?
    """, (userName,))
    formatData = [item for item in f.fetchall()[0]]
    formatData[0] = secondsToMinutes(formatData[0])
    return formatData


def secondsToMinutes(seconds):
    global minutes
    if seconds < 60:
        time = f'{minutes}.{str(round(seconds / 60, 1))[2:]}'   # [2:] to ignore 0
        minutes = 0  # clear for next session
        return time
    minutes += 1
    return secondsToMinutes(seconds - 60)


def runQuiz():  # hacky :(
    os.system('python quizSystem.py')


minutes = 0


def updateStats(userName):
    with open(quizStats, 'r') as studentSession:
        questionsCorrect = int(studentSession.readline())
        questionsAttempted = int(studentSession.readline())
        timeSpent = int(float(studentSession.readline().rstrip()))
        print(timeSpent)
        f.execute("""
                UPDATE Students
                SET 
                    questionsCorrect = questionsCorrect + ?,
                    questionsAttempted = questionsAttempted + ?,
                    timeSpent = timeSpent + ?
                WHERE userName=?
            """, (questionsCorrect, questionsAttempted, timeSpent, userName))
        file.commit()
        studentSession.close()


def refresh(userName):
    root.destroy()
    main(userName)


def main(userName):
    global root
    print('Initialising student login...')

    root = Tk()

    """
    page title
    """
    root.title(f'Student page')

    title = Label(root, text=f'Welcome, {userName}', font=('Arial', 16, 'bold'))
    title.pack()

    """
    button options
    """

    bfs = Button(root, text='Run BFS / DFS', command=lambda: [pathfinding.main()])
    bfs.pack()

    bubbleSort = Button(root, text='Run Bubble Sort', command=lambda: [sorting.main()])
    bubbleSort.pack()

    quiz = Button(root, text='Try quiz', command=lambda: [runQuiz(), updateStats(userName), refresh(userName)])  # TODO - upload stats from text file and wipe
    quiz.pack()
    if userName != 'unknownUser':
        timeSpent = Label(root, text=f'Time spent: {getStudentStats(userName)[0]} minutes', bg='white')
        questionsAttempted = Label(root, text=f'Questions attempted: {getStudentStats(userName)[1]}', bg='white')
        questionsCorrect = Label(root, text=f'Questions correct: {getStudentStats(userName)[2]}', bg='white')
        timeSpent.pack()
        questionsAttempted.pack()
        questionsCorrect.pack()

    """
    exiting
    """
    exitButton = Button(root, text="Save work", command=root.destroy)
    exitButton.pack()
    """
    main loop
    """
    root.mainloop()


if __name__ == '__main__':
    main(userName)