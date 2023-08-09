from kandinsky import draw_string
from ion import keydown, KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, KEY_OK
from random import randint


def wait_key(key):
    while keydown(key):
        pass
    while not keydown(key):
        pass


draw_string(chr(randint(97, 122)), 0, 0, "blue", "black")
draw_string("sloubi2", 10, 18, "green", "red")
wait_key(KEY_OK)
