import pyautogui as gui

def mouse_move(x,y,duration):
    gui.move(x,y,0.3)
    return 0