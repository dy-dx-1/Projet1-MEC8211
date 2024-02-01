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

data=Data(5)

Results=solver(data)
tableau_ana=graphique(data,Results)

erreurL1=erreurL1(data,data.Ntt,Results,tableau_ana)
erreurL2=erreurL2(data,data.Ntt,Results,tableau_ana)
erreurLinf=erreurLinf(data,data.Ntt,Results,tableau_ana)











