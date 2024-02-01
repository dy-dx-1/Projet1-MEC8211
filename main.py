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


Results=solver()
tableau_ana=graphique(Results)
    
#a faire les erreurs

#fonction analytique j'arrive pas a utiliser sympy pour le moment

#r = symbols('r')
#C = Function('C')(r)

erreurL1=erreurL1(Ntt,Results,tableau_ana)
erreurL2=erreurL2(Ntt,Results,tableau_ana)
erreurLinf=erreurLinf(Ntt,Results,tableau_ana)











