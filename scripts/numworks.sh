#!/usr/bin/env bash

# Ce script permet de générer des versions minifiées du fichier principal.
# Ces versions sont plus adaptées pour la calculatrice numworks étant donné son faible stockage.

MAIN_EXE=../src/main.py
OUTPUT_DIR=../numworks

echo "Attention à se mettre dans le bon répertoire avant d'effectuer cette commande. La création de la version numworks va débuter."

if [ -f $MAIN_EXE ]; then
  pyminifier --obfuscate $MAIN_EXE > $OUTPUT_DIR/pyminifier.py
  pyminify --output $OUTPUT_DIR/pyminify.py --rename-globals --remove-literal-statements $MAIN_EXE
  printf "%s " "Terminé. Appuyez sur entrée pour continuer..."
  read -r
else
  echo "Impossible de trouver $MAIN_EXE. Êtes-vous dans le bon répertoire ?"
fi