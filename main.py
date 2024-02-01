# -*- coding: utf-8 -*-
"""


@authors: 
"""
#Modules
import numpy as np
from sympy import symbols,diff,exp,sin,pi,Function
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math

#Fonctions

from erreur import erreurL1, erreurL2, erreurLinf
import data
from data import *
from graphique import *
from solver import *
from graphique_erreur import *

data_instance=Data(5)
tab_erreur=[[],[],[]]
tab_dx=[]

for n in range (1,10):
    data_instance.Ntt=5*n
    tab_dx.append(data_instance.dx)

    Results=solver(data_instance)
    tableau_ana=graphique(data_instance,Results)
    
    tab_erreur[0].append(erreurL1(data_instance,Results,tableau_ana))
    tab_erreur[1].append(erreurL2(data_instance,Results,tableau_ana))
    tab_erreur[2].append(erreurLinf(data_instance,Results,tableau_ana))


graphique_erreur(data_instance,tab_dx,tab_erreur)












