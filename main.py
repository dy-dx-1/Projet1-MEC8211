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
from solver_stationnaire import *

data_instance=Data(5)
tab_erreur=[[],[],[]]
tab_dr=[]

for n in range (1,5):
    data_instance.Ntt=5*n
    tab_dr.append(data_instance.dr)
    
    if data_instance.stationnaire == True:
        Results=solver_stationnaire(data_instance)
        tableau_ana=analytique_sur_domaine(data_instance,[i*data_instance.dr for i in range(data_instance.Ntt)])
    else:
        Results=solver(data_instance)
        tableau_ana=analytique_sur_domaine(data_instance,[i*data_instance.dr for i in range(data_instance.Ntt)])
    graphique(data_instance,Results)
    
    tab_erreur[0].append(erreurL1(data_instance,Results,tableau_ana))
    tab_erreur[1].append(erreurL2(data_instance,Results,tableau_ana))
    tab_erreur[2].append(erreurLinf(data_instance,Results,tableau_ana))


graphique_erreur(data_instance,tab_dr,tab_erreur)












