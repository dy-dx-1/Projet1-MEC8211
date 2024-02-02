# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 08:43:52 2024

@author: alsip
"""
import numpy as np
from sympy import symbols,diff,exp,sin,pi,Function
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math


def solver_stationnaire(data_instance):
    #Pour les tracer
    Results=[]
    A=np.zeros((data_instance.Ntt,data_instance.Ntt))
    A[-1][-1]=1*data_instance.unsurDeff*data_instance.dr**2
    A[0][0]=1
    A[0][1]=-1
    
    if data_instance.const == True:
        
        B=np.array([data_instance.S for i in range(data_instance.Ntt) ]).T
        B[0]=0
        B[-1]=data_instance.Ce
        
        for i in range (1,data_instance.Ntt-1):
            A[i][i-1]=1
            A[i][i]=-3
            A[i][i+1]=2
        invA=np.linalg.inv(A)*data_instance.unsurDeff*data_instance.dr**2
        
        
    else:
        B=np.array([1 for i in range(data_instance.Ntt) ]).T
        B[0]=0
        B[-1]=data_instance.Ce
        
        for i in range (1,data_instance.Ntt-1):
            A[i][i-1]=1
            A[i][i]=-3-data_instance.k*data_instance.unsurDeff*data_instance.dr**2
            A[i][i+1]=2
        invA=np.linalg.inv(A)*data_instance.unsurDeff*data_instance.dr**2
    
    Results.append(np.dot(invA,B))
    return Results