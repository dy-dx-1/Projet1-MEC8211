#!/bin/bash

# Chemin vers le fichier contenant les valeurs de poro
file_poro_values="valeurs_poro.txt"

# Chemin vers le script MATLAB original
script_matlab="launch_simulationLBM.m"

# Boucle pour parcourir les valeurs de poro
while IFS= read -r poro_value; do
    # Créer une copie temporaire du script MATLAB et le modifier avec la valeur de poro
    temp_script="${script_matlab%.m}_temp.m"
    cp "$script_matlab" "$temp_script"
    sed -i "s/poro= YYYY ;/poro= $poro_value ;/" "$temp_script"

    # Exécuter le script MATLAB temporaire
    echo "Exécution de MATLAB pour la valeur de poro : $poro_value"
    matlab -nodisplay -nodesktop -r "run('$temp_script');exit;"
    
    # Supprimer la copie temporaire du script MATLAB
    rm "$temp_script"
done < "$file_poro_values"
