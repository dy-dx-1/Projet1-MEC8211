#!/bin/bash

# Chemin vers le fichier contenant les valeurs de poro
file_poro_values="valeurs_poro.txt"

# Répertoire dédié pour les simulations avec différentes valeurs de poro
output_directory="resultats"

# Chemin vers le script MATLAB
script_matlab="~/launch_simulationLBM.m"

# Créer le répertoire de sortie s'il n'existe pas
mkdir -p "$output_directory"

# Boucle pour parcourir les valeurs de poro
while IFS= read -r poro_value; do
    # Remplacer la valeur de poro dans le script MATLAB et écrire dans le répertoire dédié
    sed "s/poro= YYYY ;/poro= $poro_value ;/" "$script_matlab" > "$output_directory/$script_matlab"
done < "$file_poro_values"
