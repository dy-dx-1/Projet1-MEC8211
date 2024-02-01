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

def graphique(data_instance,Results):
    plt.figure(1)
    X = [i*data_instance.dx for i in range(data_instance.Ntt)]
    Y = [analytique(data_instance,i) for i in X]
    plt.plot(X, Y, label='Solution analytique')
    
    
    plt.plot(X,Results[-1],label='Solution numérique')
    plt.grid(True)
    plt.xlabel('Rayon en m')
    plt.ylabel('Concentration')
    plt.title('V3 Evolution de la concentration de sel dans le pillier - {}'.format(data_instance.Ntt))
    plt.legend()
    plt.show()
    return Y