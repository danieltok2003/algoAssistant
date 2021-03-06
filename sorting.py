from tkinter import *
import threading
import random
import time
import pathfinding
from pathfinding import uploadTime

file = ''





class Sorting:
    def __init__(self, backgroundCols, foregroundCols):
        self.backgroundCols = backgroundCols  # list[coords]
        self.foregroundCols = foregroundCols  # dictionary {coords : height}

        self.windowHeight = 400
        self.windowWidth = 400
        self.cellWidth = 5
        self.cellHeight = 400
        self.visitedColor = 'red'
        self.markColor = 'yellow'
        self.correctColor = 'green'
        self.blockColor = 'purple'
        self.emptyColor = 'white'
        self.totalCols = 100
        self.maxHeight = 400

    def drawColumns(self):
        rootX = 0
        rootY = 0
        for x in range(self.totalCols):  # draws background foregroundCols
            window.create_rectangle(rootX, rootY, rootX + self.cellWidth, rootY + self.maxHeight, fill=self.emptyColor)
            window.pack()
            self.backgroundCols[x] = [rootX, rootY, rootX + self.cellWidth, rootY + self.maxHeight]
            rootX += self.cellWidth

    def randomizeHeights(self):  # randomise heights of foreground foregroundCols
        global heights
        global foreColToHeights

        for col in self.foregroundCols:  # wipes previous random iteration
            window.delete(col)
        self.foregroundCols = []
        heights = [self.cellHeight * (x / self.totalCols) for x in range(1, self.totalCols + 1)]
        random.shuffle(heights)  #  heights are drawn from top to bottom so heights will be descending to the right

        for x in self.backgroundCols:  # draws self.foregroundCols of random heights onto screen
            column = window.create_rectangle(self.backgroundCols[x][0], self.backgroundCols[x][1] + heights[x], self.backgroundCols[x][2], self.backgroundCols[x][3], fill=self.blockColor)
            self.foregroundCols.append(column)
            window.pack()  # add column to screen
        foreColToHeights = {}
        for key, val in zip(heights, self.foregroundCols):
            foreColToHeights.setdefault(val, key)

    def background_bubbleSort(self):
        bubbleSortButton["state"] = "disabled"
        threading.Thread(target=self.bubbleSort).start()

    def bubbleSort(self):
        for i in range(len(self.foregroundCols) - 1):
            for j in range(0, len(self.foregroundCols) - i - 1):
                window.itemconfig(self.foregroundCols[j], fill=self.visitedColor)
                if heights[j] > heights[j + 1]:  # if the preceding cell is taller than the following,  swap
                    window.move(self.foregroundCols[j], self.cellWidth, 0)  # swaps position of taller  cell with shorter cell
                    window.move(self.foregroundCols[j + 1], -self.cellWidth, 0)
                    heights[j], heights[j + 1] = heights[j + 1], heights[j]  # backend swapping
                    self.foregroundCols[j], self.foregroundCols[j + 1] = self.foregroundCols[j + 1], self.foregroundCols[j]
                    window.itemconfig(self.foregroundCols[j + 1], fill=self.blockColor) # recolor cells back to how they were
                else:
                    window.itemconfig(self.foregroundCols[j], fill=self.blockColor)
                time.sleep(timing)

        for colIndex in range(len(self.foregroundCols)):  # colors all blocks green when correct condition
            window.itemconfig(self.foregroundCols[colIndex], fill=self.correctColor)
        bubbleSortButton["state"] = "normal"


timing = 0

def timeControl(timeInterval):
    global timing
    timing = timeInterval


def refresh():
    master.destroy()
    main()


def main():
    global grid
    global master
    global window
    global randomizeHeights
    global bubbleSortButton
    global mergeSortButton
    grid = Sorting({}, [])

    master = Tk()
    master.resizable(False, False)
    window = Canvas(master, width=800, height=600)

    randomizeHeights = Button(master, height=1, width=15, text='Randomize Heights', command=grid.randomizeHeights)

    bubbleSortButton = Button(master, height=1, width=15, text='Bubble Sort', command=grid.background_bubbleSort)
    slow = Button(master, height=1, width=15, text='Slow', command=lambda: timeControl(0.1), bg='green')
    medium = Button(master, height=1, width=15, text='Medium', command=lambda: timeControl(0.001), bg='green')
    fast = Button(master, height=1, width=15, text='Fast', command=lambda: timeControl(0), bg='green')
    reset = Button(master, height=1, width=15, text='Reset', command=refresh)


    randomizeHeights.pack()
    bubbleSortButton.pack()
    slow.pack()
    medium.pack()
    fast.pack()
    reset.pack()
    master.after(0, grid.drawColumns())


    master.mainloop()


if __name__ == "__main__":

    main()