import login
from tkinter import *
import pathfinding
import sorting
import quizSystem
import sqlite3

file = sqlite3.connect(f'data.db')
f = file.cursor()


def getStudentStats(userName):
    f.execute("""
        SELECT timeSpent, questionsAttempted, questionsCorrect
            FROM Students S
            WHERE S.userName=?
    """, (userName,))
    return f.fetchall()[0]


def main(userName):
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

    bfs = Button(root, text='Run BFS / DFS', command=pathfinding.main)
    bfs.pack()

    bubbleSort = Button(root, text='Run Bubble Sort', command=sorting.main)
    bubbleSort.pack()

    quiz = Button(root, text='Try quiz', command=quizSystem.main)
    quiz.pack()
    if userName != 'unknownUser':
        timeSpent = Label(root, text=f'Time spent: {getStudentStats(userName)[0]} minutes', bg='white')
        questionsAttempted = Label(root, text=f'Questions attempted: {getStudentStats(userName)[1]}', bg='white')
        questionsCorrect = Label(root, text=f'Questions correct: {getStudentStats(userName)[2]}', bg='white')
        timeSpent.pack()
        questionsAttempted.pack()
        questionsCorrect.pack()





    """
    main loop
    """
    root.mainloop()


if __name__ == '__main__':
    try:
        main(userName)
    except NameError:
        main('danielTok')