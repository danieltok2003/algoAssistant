import login
from tkinter import *
import pathfinding
import sorting


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

    bfs = Button(root, text='Run BFS', command=pathfinding.main)  # split pathfinding files into bfs and dfs
    bfs.pack()

    bubbleSort = Button(root, text='Run Bubble Sort', command=sorting.main)  # split pathfinding files into bfs and dfs
    bubbleSort.pack()



    """
    main loop
    """
    root.mainloop()


if __name__ == '__main__':
    main(userName)