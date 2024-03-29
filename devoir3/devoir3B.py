# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:49:27 2024

@author: alsip
"""
from scipy import stats  
import numpy as np
import matplotlib.pyplot as plt
#Data
moyenne=0.9
ecart_type=0.0075
def monte_carlo_uniform(n):
    """tirage aléatoire de n échantillons uniforme normalisé 2D"""
    points = np.random.uniform(low=0, high=1, size=[1,n])
    return points

p_mont=monte_carlo_uniform(100)
min = moyenne - 5*ecart_type
max = moyenne + 5*ecart_type
lnspc = np.linspace(min, max, 100)
pdf = stats.norm.pdf(lnspc, moyenne, ecart_type)
cdf = stats.norm.cdf(lnspc, moyenne, ecart_type)

plt.figure()
plt.plot(lnspc, cdf, label="cdf") 
plt.xlabel('Variable')
plt.ylabel('CDF')
plt.title(' CDF pour notre variable')  
plt.legend() 
plt.savefig("CDF.png") 
plt.show()

plt.figure()
plt.plot(lnspc, pdf, label="pdf") 
plt.xlabel('Variable')
plt.ylabel('PDF')
plt.title(' PDF pour notre variable')  
plt.legend()
plt.savefig("PDF.png")  
plt.show()

ppf=stats.norm.ppf(p_mont, loc=moyenne, scale=ecart_type)

# Exporter ppf dans un fichier texte
with open('valeurs_poro.txt', 'w') as f:
    for value in ppf[0]:
        value_str = str(value).replace(',', '.')  # Remplace la virgule par un point
        f.write(f"{value_str}\n")



print(ppf)

#Post traitement

# Charger les données depuis le fichier .dat
data = np.loadtxt('poro_eff.dat')
res = np.loadtxt('k_perma.dat')
print(data)
print(len(data))
# Calculer la moyenne et l'écart type
moyenne = np.mean(res)
ecart_type = np.std(res)
median = np.median(res)

print("Moyenne :", moyenne)
print("Écart type :", ecart_type)
print("Medianne :", median)

# Calculer la CDF de vos résultats de sortie
sorted_srq = np.sort(res)
cdf = np.arange(1, len(res) + 1) / len(res)

# Tracer la CDF
plt.plot(sorted_srq, cdf)
plt.xlabel('Valeur de sortie')
plt.ylabel('Probabilité cumulative')
plt.title('CDF de la sortie (SRQ)')
plt.grid(True)
plt.show()
