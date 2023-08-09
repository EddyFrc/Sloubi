# volé sans aucune forme de respect sur github niehehehe
from keyboard import is_pressed

KEY_LEFT = 0
KEY_UP = 1
KEY_DOWN = 2
KEY_RIGHT = 3
KEY_OK = 4
KEYS = [
    "left", "up", "down", "right", "return", "del", "home", "end", None, None,
    None, None, "shift", "ctrl", ":", ";", "\"", "backspace", "[", "]",
    "{", "}", ", ", "^", "s", "c", "t", "p", "<", "²",
    "7", "8", "9", "(", ")", None, "4", "5", "6", "*",
    "/", None, "1", "2", "3", "+", "-", None, "0", ".",
    "insert", "@", "enter"
]


def keydown(key):
    if key < 0 or key > 52 or KEYS[key] is None:
        return False
    else:
        return is_pressed(KEYS[key])


def get_keys():
    return KEYS
