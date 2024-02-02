# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 13:52:53 2024

@author: alsip
"""

import numpy as np
from sympy import symbols,diff,exp,sin,pi,Function
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math

def graphique_erreur(data_instance,X,Y):
    plt.grid(True)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('dr')
    plt.ylabel('Erreur')
    plt.title('Evolution de l erreur1,2 et Inf en fonction de dr')
    for i in range(1,4): 
        y=Y[i-1]
        
        if i!=3:
            plt.plot(X, y,label='ErreurL{}'.format(i))
        else:
            plt.plot(X, y,label='ErreurLinf')
    plt.legend()
    plt.show()