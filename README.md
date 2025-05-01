# Sloubi 2

... est un jeu d'arcade très simple dans lequel vous contrôlez un petit carré bleu, et devez éviter les carrés rouges. Ce jeu a la particularité de tourner nativement sur la calculatrice "Numworks", mais peut être également installé sur Windows.

## Installation

### Numworks

Importez le script depuis [le site my.numworks.com](https://bit.ly/sloubi_2_latest). C'est la version minifiée du jeu, la même que dans `numworks/sloubi2.min.py`.

### Windows

Téléchargez l'exécutable depuis <a>https://github.com/EddyFrc/Sloubi/releases</a> (x86_64 uniquement).

### Autres plateformes

Il est possible de faire tourner le jeu sans "l'empaqueter" en exécutable, simplement en exécutant `src/main.py` avec l'interpréteur Python, après avoir installé toutes les dépendances. Pour cela, clonez le projet avec `git`. L'interpréteur et les dépendances ne sont pas fournies.

# Structure

* `src` : L'intégralité du code source se trouve dans `src/main.py`
* `numworks` : Fichiers minifiés générés à partir de différents algorithmes, dont certains modifiés à la main après coup
* `graphics` : Icône du jeu en différents formats (`.ico` utilisé pour les versions PC)
* `scripts` : Scripts utilitaires écrits en différents shells permettant de générer des exécutables ou des versions minifiées<br>
  Note : Il peut être nécessaire de créer le dossier `build_win` avant de générer un exécutable pour Windows.

## Dépendances

Nom du paquet      | Lien                                             | Facultatif | Notes
-------------------|--------------------------------------------------|------------|-----------------------------
`ion-numworks`     | <a>https://pypi.org/project/ion-numworks</a>     | Non        | Détection des touches
`kandinsky`        | <a>https://pypi.org/project/kandinsky</a>        | Non        | Affichage du jeu (interface)
`win-precise-time` | <a>https://pypi.org/project/win-precise-time</a> | Oui        | Uniquement sur Windows

# Si vous êtes développeur

Pour construire un exécutable, utilisez pyinstaller ou similaire (pour les scripts, attention à bien remplacer les chemins, cela fonctionne uniquement pour moi). Attention cependant, il faut rajouter toutes les dépendances non-incluses ici. Si vous ne voulez pas vous embêter, il y a toujours les releases (à l'heure où j'écris, la version PC est uniquement pour Windows). Celles-ci regroupent deux fichiers :

* La version pour calculatrice **Numworks** : un simple fichier source python, réduit au maximum pour économiser le moindre octet (c'est important, car la mémoire est extrêmement limitée). Si vous voulez l'installer, je vous conseille cependant d'utiliser [la page du site my.numworks.com](https://bit.ly/sloubi_2_latest). Je doute même qu'une autre méthode soit possible.
* La version pour **Windows** : un exécutable.

Pour modifier les paramètres de base au delà de ce que permet le jeu, changez les constantes définies dans `main.py`. Je ne pense pas que ce soit nécessaire d'expliquer le nom de tous les paramètres. Si besoin, contactez-moi.
