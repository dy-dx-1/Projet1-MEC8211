# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 12:06:11 2024

@author: alsip
"""
from data import *

def analytique(r):
    return 0.25*S/Deff*0.5**2*((r*2)**2-1) + Ce