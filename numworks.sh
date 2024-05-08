#!/bin/env zsh
echo "Attention à se mettre dans le bon répertoire avant d'effectuer cette commande. La création de la version numworks va débuter."
pyminifier --obfuscate ./src/main.py > ./numworks/pyminifier.py
pyminify --output ./numworks/pyminify.py --rename-globals --remove-literal-statements ./src/main.py
printf "%s " "Terminé. Appuyez sur entrée pour continuer..."
read ans