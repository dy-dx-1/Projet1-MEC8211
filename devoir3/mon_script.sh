#!/bin/bash

# Chemin vers le fichier contenant les valeurs de poro
file_poro_values="valeurs_poro.txt"

# Chemin vers le script MATLAB
script_matlab="launch_simulationLBM.m"

# Boucle pour parcourir les valeurs de poro
while IFS= read -r poro_value; do
    # Remplacer la valeur de poro dans le script MATLAB et écrire dans le répertoire dédié
    sed "s/poro= YYYY ;/poro= $poro_value ;/" "$script_matlab" 
done < "$file_poro_values"
