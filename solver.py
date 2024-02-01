# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:44:14 2024

@author: alsip
"""
import numpy as np
from sympy import symbols,diff,exp,sin,pi,Function
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math

#fonctions


def solver(data_instance):
    #Pour les tracer
    Results=[]
    #pour les boucles
    t=0
    #Constante de la matrice
    alpha = 1 +3*data_instance.Deff*data_instance.unsurdx**2*data_instance.dt
    beta = -2*data_instance.Deff*data_instance.unsurdx**2*data_instance.dt
    delta = -1*data_instance.Deff*data_instance.unsurdx**2*data_instance.dt
    
    #Initialisation
    gamma0=np.zeros((data_instance.Ntt,1))
    gamma0[-1][0]=data_instance.Ce
    Results.append(gamma0)
    
    unit=np.ones((data_instance.Ntt,1))
    #Configuration de A cas constant
    
    A=np.zeros((data_instance.Ntt,data_instance.Ntt))
    A[-1][-1]=1
    A[0][0]=-3
    A[0][1]=4
    A[0][2]=-1
    
    for i in range (1,data_instance.Ntt-1):
        A[i][i-1]=beta
        A[i][i]=alpha
        A[i][i+1]=delta
        
    invA=np.linalg.inv(A)
    
    #Cas constante
    if data_instance.const == True:
        while t<data_instance.itermax:
            t+=1
            gamma0=np.dot(invA,gamma0)-data_instance.S*data_instance.dt*np.dot(invA,unit)
            Results.append(gamma0)
    
    #Cas non constante
    if data_instance.const != True:
        invA=np.linalg.inv(A-data_instance.k*data_instance.dt*np.eye(5))
        while t<data_instance.itermax:
            gamma0=np.dot(invA,gamma0)
            Results.append(gamma0)
        

    return Results