# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:47:44 2024

@author: alsip
"""

def erreurL1(nbr_noeuds,Results,tableauf):
    erreur = 0
    for i in range(nbr_noeuds):
        erreur+=Results[-1][i]-tableauf[i]
    return erreur

def erreurL2(nbr_noeuds,Results,tableauf):
    erreur = 0
    for i in range(nbr_noeuds):
        erreur+=(Results[-1][i]-tableauf[i])**2
    return erreur**(1/2)

def erreurLinf(nbr_noeuds,Results,tableauf):
    erreur=[Results[-1][i]-tableauf[i] for i in range(nbr_noeuds)]
    return max(erreur)
