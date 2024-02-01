# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:47:44 2024

@author: alsip
"""
import math 

def erreurL1(data_instance,Results,tableauf):
    erreur = 0
    for i in range(data_instance.Ntt):
        erreur+=abs(Results[-1][i]-tableauf[i])
    return erreur

def erreurL2(data_instance,Results,tableauf):
    erreur = 0
    for i in range(data_instance.Ntt):
        erreur+=(Results[-1][i]-tableauf[i])**2
    return erreur**(1/2)

def erreurLinf(data_instance,Results,tableauf):
    erreur=[-1*(Results[-1][i]-tableauf[i]) for i in range(data_instance.Ntt)]
    return max(erreur)
