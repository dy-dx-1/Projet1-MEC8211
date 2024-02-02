# -*- coding: utf-8 -*-
"""
Created on Thu Feb 1 12:06:11 2024

@author: alsip
"""

def analytique(data_instance, r):
    """
    Fonction analytique pour le calcul de la concentration.

    Parameters
    ----------
    data_instance : Data
        Instance de la classe Data.
    r : float
        Rayon.

    Returns
    -------
    float
        Valeur de concentration calculée analytiquement.

    """
    return 0.25 * (data_instance.S / data_instance.Deff) * 0.5**2 * ((r * 2)**2 - 1) + data_instance.Ce

def analytique_sur_domaine(data_instance, domaine):
    """
    Fonction analytique pour le calcul de la concentration sur un domaine donné.

    Parameters
    ----------
    data_instance : Data
        Instance de la classe Data.
    domaine : list
        Liste des valeurs de rayon.

    Returns
    -------
    list
        Liste des valeurs de concentration calculées analytiquement.

    """
    return [analytique(data_instance, i) for i in domaine]