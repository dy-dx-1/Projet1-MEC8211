# -*- coding: utf-8 -*-
"""


@authors: 
"""
import numpy as np


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
itermax=100000
t=0

#Pour les tracer
Results=[]

#Constante de la matrice
alpha = 1 +3*Deff*unsurdx**2*dt
beta = -2*Deff*unsurdx**2*dt
delta = -1*Deff*unsurdx**2*dt

#Initialisation
gamma0=np.zeros((5,1))
gamma0[4][0]=Ce
Results.append(gamma0)
#Configuration de A cas constant

A=np.zeros((5,5))
A[4][4]=1
A[0][0]=-1
A[0][1]=1
for i in range (1,4):
    A[i][i-1]=beta
    A[i][i]=alpha
    A[i][i+1]=delta
    
invA=np.linalg.inv(A)

#Cas constante
if const == True:
    while t<itermax:
        t+=1
        gamma0=invA*gamma0-S*dt*invA
        Results.append(gamma0)

#Cas non constante
if const != True:
    while t<itermax:
        invA=np.linalg.inv(A-k*dt*np.eye(5))
        gamma0=invA*gamma0
        Results.append(gamma0)
        
        
#a faire les erreurs


        
        
    












