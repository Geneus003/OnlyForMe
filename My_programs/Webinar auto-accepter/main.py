import mouse
import keyboard
import os
from threading import Thread
import time
import win32gui

a = True
temp_hwnd = None


def wait_user_input():
    global a
    keyboard.wait("ctrl+m")
    a = False


def find_browser_window():
    def win_enum_handler(hwnd, ctx):
        global temp_hwnd
        if win32gui.IsWindowVisible(hwnd):
            if "Webinar.ru" in win32gui.GetWindowText(hwnd):
                temp_hwnd = hwnd

    win32gui.EnumWindows(win_enum_handler, None)


def main():
    global a
    wait_leave_input = Thread(target=wait_user_input)
    wait_leave_input.start()

    while True:
        find_browser_window()
        if temp_hwnd is None:
            print("Откройте ваш браузер с лекцией на Webinar.ru, как активное окно")
            find_browser_window()
            time.sleep(0.5)
        else:
            break

    while a:
        print(temp_hwnd, win32gui.GetWindowText(temp_hwnd))
        time.sleep(1)


if __name__ == "__main__":
    main()
