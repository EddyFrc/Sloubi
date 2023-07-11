# Sloubi 2

... est un jeu d'arcade très simple dans lequel vous contrôlez un petit carré bleu, et devez éviter les carrés rouges. Ce jeu a la particularité de tourner nativement sur la calculatrice "Numworks", mais peut être également installé sur Windows.

Le jeu "en brut" est dans ``src/main.py``. 

Le jeu tel qu'il devrait être importé sur calculatrice se trouve [ici](https://bit.ly/sloubi_2_latest). Passez par cet endroit si vous voulez l'importer, donc (il y a même un bouton pour le faire automatiquement, et je doute qu'une autre méthode soit possible d'ailleurs).

Pour compiler, utiliser pyinstaller ou similaire. Attention cependant, il faut rajouter toutes les dépendances non-incluses ici. Si vous ne voulez pas vous embêter, il y a toujours les releases (s'il n'y en a pas, juste un peu de patience, j'y travaille). Celles-ci seront séparées en deux fichiers :

* La version pour calculatrice **Numworks** : un simple fichier python, réduit au maximum pour économiser le moindre octet (c'est important, car la mémoire est extrêmement limitée). Si vous voulez l'installer, je vous conseille cependant d'utiliser [la page du site my.numworks.com](https://bit.ly/sloubi_2_latest).
* La version pour **Windows** : un exécutable.

L'icône du jeu utilisée pour la version Windows est disponible dans le dossier ``graphics``.

Pour modifier les paramètres de base (dans cette version en tout cas, je prévois de rendre possible les arguments en cli), modifier cette ligne dans ``main.py`` :
```python
Struct.main(base_player_x_pos=160.0, base_player_y_pos=120.0, base_player_speed=1.0, base_player_size=10.0,
            base_player_color=(0, 0, 0), base_obstacles=[], base_dif=1, base_speed=1.0, first_tick=0, base_fps=40.0)
```
Je ne pense pas que ce soit nécessaire d'expliquer le nom de tous les paramètres ci-dessus. Si besoin, contactez-moi.

Je crois que c'est à peu près tout.