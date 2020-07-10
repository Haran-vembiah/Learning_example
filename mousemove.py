import pyautogui
i=0
while True:
    i += 1
    pyautogui.moveTo(100+i, 100, duration=0.25)
    pyautogui.moveTo(100+i, 200, duration=0.25)
    pyautogui.moveTo(300+i, 200, duration=1)
    pyautogui.keyDown('Esc')
    continue


