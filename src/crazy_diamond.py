# A exécuter si la fenêtre de kandisky est buggée, on dirait que ça marche (probablement grâce au quit())
from kandinsky import draw_string, quit
from time import sleep

draw_string("Réparation du module...", 0, 0)
sleep(1)
quit()