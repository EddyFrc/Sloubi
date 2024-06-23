#!/bin/env zsh
cd $(dirname $(realpath $0))
echo "Attention à se mettre dans le bon répertoire avant d'effectuer cette commande. La création de l'exécutable va débuter."
pyinstaller --onefile --windowed --icon "./graphics/icon.ico" --name "sloubi-linux-x86_64" --add-data "./src/ion.py:." --add-data "./graphics/icon.ico:." --add-data "../.venv/lib/python3.11/site-packages/kandinsky:kandinsky" "./src/main.py"
printf "%s " "Terminé. Appuyez sur entrée pour continuer..."
read ans