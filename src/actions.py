from enum import Enum
import os
from automations import click, click_key, type, get_selected_text
from design import Item, Job

WINDOWS = os.name == "nt"
    
class KEYS(Enum):
    enter = "enter" if WINDOWS else "return"
    tab = "tab"
    shift_tab = ("shift", "tab")
    ctrl_tab = ("ctrl" if WINDOWS else "command", "tab")
    right = "right"
    down = "down"

    
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


def get_item_job(item_number: str, asset_position: tuple[int, int], testing_position: tuple[int, int], job: Job | None = None) -> tuple[Item, Job]:
    click()
    type(item_number)
    click_key(KEYS.enter.value)
    click(asset_position)
    click_key(KEYS.tab.value)
    type(item_number)
    click_key(KEYS.enter.value)
    click_key(KEYS.tab.value, times=7)
    serial = get_selected_text()
    click_key(KEYS.tab.value)
    model = get_selected_text()
    click_key(KEYS.tab.value, times=2)
    description = get_selected_text()
    click_key(KEYS.tab.value, times=2)
    manufacturer = get_selected_text()

    item = Item(item_number, description, model, manufacturer, "None", "None", serial)

    click_key(KEYS.tab.value)
    company = get_selected_text()
    click_key(KEYS.tab.value)
    campus = get_selected_text()
    click_key(KEYS.tab.value)
    department = get_selected_text()
    click_key(KEYS.tab.value, times=21)
    click_key(KEYS.enter.value)

    click(testing_position)

    if job is None:
        job = Job(company, campus, department)

    return item, job



    