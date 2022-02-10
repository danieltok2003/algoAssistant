from tkinter import *
import sqlite3
import re
import random
import time

"""
TODO
1. get input from user - count questions correct 
2. count time taken
3. count questions attempted
"""
questionFile = 'questions'
quizQuestions = {}
correct = 0
attempted = 0
choice = False
file = 'studentSession'


class Component:
    def __init__(self, root):
        self.root = root

    def getQuestionData(self):
        with open(questionFile, 'r') as questions:
            for line in questions:
                question = re.search(r'(.*)\?', line)  # extract all characters before first ? symbol

                options = [item.strip() for item in (re.search(r'\*(.*)\*', line)).group(1).split(',')]
                # extracts options between the * *, group(1) to remove * * boundary characters,
                # split options into list separated by ,
                # item.strip() to trim trailing and ending spaces from options
                quizQuestions[question.group().replace("\x00", "")] = options  # question.group() as want to include ? at end of string
        return quizQuestions

    def clearFrame(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()


class quizLabel(Component):
    def __init__(self, root):
        super().__init__(root)

    def drawQuestion(self, question):
        Label(self.root, text=question).pack()


class quizButton (Component):
    def __init__(self, root):
        super().__init__(root)

    def drawButton(self, option, correct):
        if correct is None:  # submit button case
            item = Button(self.root, text=option, bg='green',
                        command=lambda: [submitClicked.set(1), self.clearFrame(), checkCorrect()])

        elif correct is True:  # correct answer buttons
            item = Button(self.root, text=option, command=choiceCorrect)
        else:  # incorrect answer buttons
            item = Button(self.root, text=option, command=choiceIncorrect)
        return item


def randomizeOrder(A, B, C, D):
    buttons = [A, B, C, D]
    random.shuffle(buttons)
    for item in buttons:
        item.pack()


def choiceCorrect():
    global choice
    choice = True
    return choice


def choiceIncorrect():
    global choice
    choice = False
    return choice


def checkCorrect():
    if choice is True:
        incrementCorrect()
        incrementAttempted()
    else:
        incrementAttempted()


def incrementCorrect():
    global correct
    correct += 1
    return correct


def incrementAttempted():
    global attempted
    attempted += 1
    return attempted




def main():
    global submitClicked
    root = Tk()
    root.geometry("500x200")

    submitClicked = IntVar()

    """
    page title
    """
    root.title(f'Quiz page')

    questions = Component(root).getQuestionData().keys()

    print(questions)
    start_time = time.time()
    for key in questions:

        quizLabel(root).drawQuestion(key)
        optionA = quizButton(root).drawButton(quizQuestions[key][0], True)
        optionB = quizButton(root).drawButton(quizQuestions[key][1], False)
        optionC = quizButton(root).drawButton(quizQuestions[key][2], False)
        optionD = quizButton(root).drawButton(quizQuestions[key][3], False)

        randomizeOrder(optionA, optionB, optionC, optionD)

        submitButton = quizButton(root).drawButton('submit', None)
        submitButton.pack()
        submitButton.wait_variable(submitClicked)
    with open(file, 'w') as studentSession:  # opening as 'w' clears file for new session
        studentSession.write(str(correct) + '\n')
        studentSession.write(str(attempted) + '\n')
        studentSession.write(str(round(time.time() - start_time, 0)) + '\n')
        studentSession.close()


if __name__ == "__main__":
    main()