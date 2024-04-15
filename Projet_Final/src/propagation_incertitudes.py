# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:49:27 2024

@author: alsip
"""
from scipy import stats  
import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_uniform(n):
    """tirage aléatoire de n échantillons uniforme normalisé 2D"""
    points = np.random.uniform(low=0, high=1, size=[1,n])
    return points

# Paramètres de la distribution log-normale
moyenne = 0  # La moyenne en échelle log
ecart_type = 0.25  # L'écart type en échelle log
min_rayon = 0.00001
max_rayon = 5

# Générer des échantillons
nb_echantillons = 10000
rayons_lognormal = np.random.lognormal(mean=moyenne, sigma=ecart_type, size=nb_echantillons)

# Afficher l'histogramme des rayons
plt.hist(rayons_lognormal, bins=50, density=True, alpha=0.6, color='g')

# Afficher la densité de probabilité théorique
x = np.linspace(min_rayon, max_rayon, 100)
y = (1 / (x * ecart_type * np.sqrt(2 * np.pi))) * np.exp(-(np.log(x) - moyenne)**2 / (2 * ecart_type**2))
plt.plot(x, y, color='r', linewidth=2)

plt.xlabel('U_inf (m/s)')
plt.ylabel('Densité de probabilité')
plt.title('Distribution log-normale de U_inf')
plt.grid(True)
plt.savefig("Histograme")
plt.show()


p_mont=monte_carlo_uniform(100)

# Transformer les échantillons uniformes en échantillons log-normaux
echantillons = stats.lognorm.ppf(p_mont, ecart_type, np.exp(moyenne))

print(echantillons)
print("version liste",echantillons.tolist()[0])


# # Exporter ppf dans un fichier texte
# with open('rayons.txt', 'w') as f:
#     for value in echantillons[0]:
#         value_str = str(value).replace(',', '.')  # Remplace la virgule par un point
#         f.write(f"{value_str}\n")



# # traitement des résultats
# res=[]
# # Calculer la moyenne et l'écart type
# moyenne = np.mean(res)
# ecart_type = np.std(res)
# median = np.median(res)

# print("Moyenne :", moyenne)
# print("Écart type :", ecart_type)
# print("Medianne :", median)

# # Calculer la CDF de vos résultats de sortie
# sorted_srq = np.sort(res)
# cdf = np.arange(1, len(res) + 1) / len(res)

# # Tracer la CDF
# plt.plot(sorted_srq, cdf)
# plt.xlabel('Valeur de sortie')
# plt.ylabel('Probabilité cumulative')
# plt.title('CDF de la sortie (SRQ)')
# plt.grid(True)
# plt.show()
