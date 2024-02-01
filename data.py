# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:50:58 2024

@author: alsip
"""

#Constantes
Deff = 10e-10
L = 0.5
Ce = 12


Ntt = 5
dx=L/Ntt
unsurdx=1/dx

#Si S n'est pas constant decomentez les lignes suivantes
S = 8*10e-9
k = 4*10e-9
const = True

#Valeur pour la boucle temporelle
dt=1e-5 #pas précisé
itermax=10000
