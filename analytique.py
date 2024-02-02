# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 12:06:11 2024

@author: alsip
"""


def analytique(data_instance,r):
    return 0.25*(data_instance.S/data_instance.Deff)*0.5**2*((r*2)**2-1) + data_instance.Ce

def analytique_sur_domaine(data_instance,domaine):
    return [analytique(data_instance,i) for i in domaine]