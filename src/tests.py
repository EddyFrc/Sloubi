from kandinsky import *
from ion import *
from time import sleep

fill_rect(0, 0, 40, 40, "white")

if keydown(KEY_DOWN):
    fill_rect(0, 0, 40, 40, "blue")
    sleep(4)

quit()