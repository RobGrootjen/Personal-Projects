import pyautogui
import time
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import os

#Root
root = Tk()
root.title("Groot's AutoDragger")
root.geometry('350x240')

#Define repetitions
def repsNeeded():
    getRep = repsInput.get()
    return(getRep)

#Repetitions
reps = Label(root, text="Repeat quantity:")
reps.place(x=10,y=10)

#Reps input
repsInput = Entry(root, width=6, show=None, font=('Arial',13))
repsInput.place(x=100,y=10)

#Message instruction
messageHow = LabelFrame(root, text='Instructions',bg='white')
messageHow.place(x=10,y=40)

#Instruction 1
instructionOne = Label(messageHow, text="1. Put in the amount of how many candidates you will drag. \n \n2. Click 'Save Criteria'. \n \n3.Click 'Start dragging' and put your mouse for 5 seconds \non the first candidate where you will be dragging from. \n \n4. Now LEAVE your mouse on the day you will be dragging \neverything to and the process will start automatically. \n \n5. Don't touch mouse untill process is finished.",bd=1,relief='solid',font='Times 10',width=46,height=11,anchor=W,justify=LEFT,bg='white')
instructionOne.pack()

#Save searchcriteria button
saveReps = Button(root, text = 'Save criteria', command=repsNeeded)
saveReps.place(x=165,y=7.5)

def startDrag():
    #Get repeat variable
    time.sleep(1)
    repeat = repsNeeded()
    repeat = int(repeat)
    
    #Get position 1
    time.sleep(3)
    currentPosition1 = pyautogui.position()

    #Get position 2(Where you want to drag the candidates)
    time.sleep(8)
    currentPosition2 = pyautogui.position()

    #Start process.
    def autoMouse(x,y):
        for i in range(repeat):
            time.sleep(0.1)
            pyautogui.moveTo(x)
            pyautogui.mouseDown(button='left')
            pyautogui.moveTo(y)
            time.sleep(0.1)
            pyautogui.mouseUp(button='left')

    autoMouse(currentPosition1,currentPosition2)

    #Done
    print('Done!')

#Start dragging button
startButton = Button(root, text='Start dragging',command=startDrag)
startButton.place(x=240,y=7.5)

#Loop
root.mainloop()
