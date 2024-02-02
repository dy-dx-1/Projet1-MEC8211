# -*- coding: utf-8 -*-
"""
@authors: alcaru
"""

# Fonctions
from erreur import erreur_L1, erreur_L2, erreur_Linf
from data import Data
from graphique import graphique
from solver import solver
from graphique_erreur import graphique_erreur
from solver_stationnaire import solver_stationnaire
from analytique import analytique_sur_domaine

data_instance=Data(5)
tab_erreur=[[],[],[]]
tab_dr=[]

for n in range(1, 3):
    data_instance.Ntt = 5 * n
    tab_dr.append(data_instance.dr)

    if data_instance.stationnaire:
        Results = solver_stationnaire(data_instance)
        tableau_ana = analytique_sur_domaine(
            data_instance, [i * data_instance.dr for i in range(data_instance.Ntt)]
        )
    else:
        Results = solver(data_instance)
        tableau_ana = analytique_sur_domaine(
            data_instance, [i * data_instance.dr for i in range(data_instance.Ntt)]
        )
    graphique(data_instance, Results)

    tab_erreur[0].append(erreur_L1(data_instance, Results, tableau_ana))
    tab_erreur[1].append(erreur_L2(data_instance, Results, tableau_ana))
    tab_erreur[2].append(erreur_Linf(data_instance, Results, tableau_ana))

graphique_erreur(data_instance, tab_dr, tab_erreur)












