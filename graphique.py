# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:59:25 2024

@author: alsip
"""
import numpy as np
from sympy import symbols,diff,exp,sin,pi,Function
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math



from analytique import *

def graphique(data,Results):
    plt.figure(1)
    X = [i for i in range(data.Ntt)]
    Y = [analytique(data,i) for i in X]
    plt.plot(X, Y)
    
    
    plt.plot(X,Results[-1])
    plt.grid(True)
    plt.xlabel('Noeuds')
    plt.ylabel('Concentration')
    plt.title('V3 Evolution de la concentration de sel dans le pillier (1D)')
    plt.show()
    return Y