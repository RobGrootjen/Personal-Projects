import pyautogui
import time
import os


def startDrag(x):
    #Get repeat variable
    time.sleep(1)
    repeat = x
    repeat = int(repeat)

    #Get position 1
    time.sleep(3)
    currentPosition1 = pyautogui.position()
    print('Done, next!')

    #Get position 2(Where you want to drag the candidates)
    time.sleep(8)
    currentPosition2 = pyautogui.position()

    #Start process.
    def autoMouse(x,y):
        for i in range(repeat):

            pyautogui.moveTo(x)
            time.sleep(0.45)
            pyautogui.mouseDown(button='left')
            time.sleep(0.45)

            pyautogui.moveTo(y)
            time.sleep(0.45)
            pyautogui.mouseUp(button='left')
            time.sleep(0.45)


    autoMouse(currentPosition1,currentPosition2)

    #Done
    print('Done!')

startDrag(1163)
