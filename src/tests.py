from kandinsky import fill_rect
from time import sleep

for y in range(20):
    for i in range(20):
        fill_rect(i * 10, y * 10, 10, 10, (i * 12, 250 - i * 12, y * 12))
        sleep(1 / 60.0)

quit()