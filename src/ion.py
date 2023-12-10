from pynput import keyboard

KEY_LEFT = 0
KEY_UP = 1
KEY_DOWN = 2
KEY_RIGHT = 3
KEY_OK = 4
KEYS = [
    "left", "up", "down", "right", "enter", "del", "home", "end", None, None,
    None, None, "shift", "ctrl", ":", ";", "\"", "backspace", "[", "]",
    "{", "}", ", ", "^", "s", "c", "t", "p", "<", "²",
    "7", "8", "9", "(", ")", None, "4", "5", "6", "*",
    "/", None, "1", "2", "3", "+", "-", None, "0", ".",
    "insert", "@", "enter"
]

pressed_keys = [False] * 53

def keydown(key):
    if key < 0 or key > 52 or KEYS[key] is None:
        return False
    else:
        return pressed_keys[key]

def get_keys():
    return KEYS

def on_press(key):
    try:
        pressed_keys[KEYS.index(key.name)] = True
    except AttributeError:
        pass
    except ValueError:
        pass

def on_release(key):
    try:
        pressed_keys[KEYS.index(key.name)] = False
    except AttributeError:
        pass
    except ValueError:
        pass

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
