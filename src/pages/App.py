import time
import tkinter
from tkinter import ttk
from typing import Any

import pyautogui

from pages.JobPage import JobPage
from pages.Page import TPAGES, Page
from pages.TestPage import TestPage

from design.Job import Job

"""
['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&',
"'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', 
'3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', 
'?', '@', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 
'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 
't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'accept', 'add', 
'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback', 'browserfavorites', 
'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 
'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 
'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10', 
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 
'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 
'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 
'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'left', 'modechange',
'multiply', 'nexttrack', 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5',
'num6', 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 
'return', 'right', 'scrolllock', 'select', 'separator', 'shift', 'shiftleft', 'shiftright', 
'sleep', 'space', 'stop', 'subtract', 'tab', 'up', 'volumedown', 'volumemute', 'volumeup', 
'win', 'winleft', 'winright', 'yen', 'command', 'option', 'optionleft', 'optionright']
"""

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        maxWidth = self.winfo_screenwidth()
        width = 360
        height = self.winfo_screenheight()
        self.geometry(f"{width}x{height}+{maxWidth - width}+0")
        self.title("ALTER SMX Tool")
        self.attributes("-topmost", 1)  # type: ignore

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.jobs: list[Job] = []

        self.pages: dict[TPAGES, Page] = {
            "JOB": JobPage(self._frame(), self.change_page, jobs=self.jobs), 
            "TEST": TestPage(self._frame(), self.change_page),
        }
        self.current_page: Page | None = None
        self.change_page("JOB")

    def _frame(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding="3 3 12 12")
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        return frame

    def change_page(self, page: TPAGES, **kwargs: Any):
        if self.current_page is not None:
            self.current_page.frame.grid_remove()
            for widget in self.current_page.frame.winfo_children():
                widget.grid_remove()

        self.current_page = self.pages[page]
        self.current_page.setup(**kwargs)
        self.current_page.frame.grid(row=0, column=0, sticky="nsew")


def google_search(query: str):
    # Wait for a moment before starting the automation
    time.sleep(5)

    # Open the Start menu or Spotlight (macOS) to search for the web browser
    with pyautogui.hold("command"):
        pyautogui.press("space")
    pyautogui.printInfo()
    # pyautogui.typewrite('chrome')
    # pyautogui.press('enter')

    # # Wait for the web browser to open
    # time.sleep(5)

    # # Type the search query into the address bar
    # pyautogui.typewrite(f'https://www.google.com/search?q={query}')
    # pyautogui.press('enter')

    # # Wait for the search results to load
    # time.sleep(5)

    # # Scroll down to see more results (optional)
    # pyautogui.scroll(-2)


if __name__ == "__main__":
    app = App()
    app.mainloop()
