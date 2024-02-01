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

data_instance=Data(5)
tab_erreurL1=[]
tab_erreurL2=[]
tab_erreurLinf=[]

for n in range (1,10):
    data_instance.Ntt=5*n

    Results=solver(data_instance)
    tableau_ana=graphique(data_instance,Results)
    
    tab_erreurL1.append(erreurL1(data_instance,data_instance.Ntt,Results,tableau_ana))
    tab_erreurL2.append(erreurL2(data_instance,data_instance.Ntt,Results,tableau_ana))
    tab_erreurLinf.append(erreurLinf(data_instance,data_instance.Ntt,Results,tableau_ana))












