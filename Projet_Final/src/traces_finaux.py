import matplotlib.pyplot as plt
import numpy as np
import math as math

Exp=np.array([0.03014586398906757, -0.0008577538117113107])
Sim=np.array([ 0.030402234656496253,-0.0020319872516330008])

trace=[0.00025637066742868406,0.00025637066742868406,0.00117423343992169,0.00117423343992169]
print(trace)

# Définition des valeurs et de leurs incertitudes pour chaque cas
valeurs = trace
Unum1=5.2e-5
Unum2=1.3e-4
Ud=1e-4
Uval1=(Ud**2+Unum1**2)**0.5
Uval2=(Ud**2+Unum2**2)**0.5

incertitudes = [4*Unum1, 4*Uval1, 4*Unum2,4*Uval2]
couleurs = ['darkblue', 'blue', 'darkred','red']

# Création du graphique pour chaque cas
for i in range(4):
    plt.errorbar(i + 1, valeurs[i], yerr=incertitudes[i], fmt='o', capsize=5, color=couleurs[i], markersize=8)

# Ajout d'une ligne en pointillés à zéro
plt.axhline(y=0, color='black', linestyle='--')

# Ajout des étiquettes pour chaque cas au niveau de l'axe des abscisses
plt.xticks([1, 2, 3, 4], ['Cd sans Ud', 'Cd avec Ud', 'Cl sans Ud', 'Cd avec Ud'])

# Ajout du titre et des labels d'axes
plt.title('Graphique avec incertitudes')
plt.xlabel('Situations')
plt.ylabel('Δ(deltamodele)')
plt.savefig('graphique_final.png')
# Affichage du graphique
plt.show()
