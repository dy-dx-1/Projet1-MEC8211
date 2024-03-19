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

p_mont=monte_carlo_uniform(1000)
min = moyenne - 5*ecart_type
max = moyenne + 5*ecart_type
lnspc = np.linspace(min, max, 1000)
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
with open('valeur_poro.txt', 'w') as f:
    for value in ppf[0]:
        value_str = str(value).replace(',', '.')  # Remplace la virgule par un point
        f.write(f"{value_str}\n")



print(ppf)
