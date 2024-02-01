# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 12:06:11 2024

@author: alsip
"""


def analytique(data,r):
    return 0.25*data.S/data.Deff*0.5**2*((r*2)**2-1) + data.Ce