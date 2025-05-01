# Sloubi 2

... est un jeu d'arcade très simple dans lequel vous contrôlez un petit carré bleu, et devez éviter les carrés rouges. Ce jeu a la particularité de tourner nativement sur la calculatrice "Numworks", mais peut être également installé sur Windows.

L'intégralité du code source se trouve dans `src/main.py`. 

Le jeu tel qu'il devrait être importé sur calculatrice se trouve [ici](https://bit.ly/sloubi_2_latest). Passez par cet endroit si vous voulez l'importer, donc (il y a même un bouton pour le faire automatiquement, et je doute qu'une autre méthode soit possible d'ailleurs). C'est la version minifiée du jeu, la même que dans `numworks/sloubi2.min.py`.

Pour construire un exécutable, utiliser pyinstaller ou similaire. Attention cependant, il faut rajouter toutes les dépendances non-incluses ici. Si vous ne voulez pas vous embêter, il y a toujours les releases (à l'heure où j'écris, uniquement pour Windows). Celles-ci regroupent deux fichiers :

* La version pour calculatrice **Numworks** : un simple fichier python, réduit au maximum pour économiser le moindre octet (c'est important, car la mémoire est extrêmement limitée). Si vous voulez l'installer, je vous conseille cependant d'utiliser [la page du site my.numworks.com](https://bit.ly/sloubi_2_latest).
* La version pour **Windows** : un exécutable.

L'icône du jeu utilisée pour la version Windows est disponible dans le dossier ``graphics``.

Pour modifier les paramètres de base au delà de ce que permet le jeu, changez les constantes définies dans `main.py`. Je ne pense pas que ce soit nécessaire d'expliquer le nom de tous les paramètres. Si besoin, contactez-moi.
