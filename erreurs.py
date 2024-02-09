# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:47:44 2024

@author: alsip
"""
def erreur_L1(data_instance, results, tableau_f):
    """
    Fonction permettant de calculer l'erreur L1.

    Parameters
    ----------
    data_instance : TYPE class
        DESCRIPTION.
    results : TYPE tableau numpy
        DESCRIPTION.
    tableau_f : TYPE tableau numpy
        DESCRIPTION.

    Returns
    -------
    erreur : float
        Erreur L1 calculée.

    """
    erreur = 0
    for i in range(data_instance.N):
        erreur += abs(results[-1][i] - tableau_f[i])
    return erreur

def erreur_L2(data_instance, results, tableau_f):
    """
    Fonction permettant de calculer l'erreur L2.

    Parameters
    ----------
    data_instance : TYPE class
        DESCRIPTION.
    results : TYPE tableau numpy
        DESCRIPTION.
    tableau_f : TYPE tableau numpy
        DESCRIPTION.

    Returns
    -------
    erreur : float
        Erreur L2 calculée.

    """
    erreur = 0
    for i in range(data_instance.N):
        erreur += (results[-1][i] - tableau_f[i]) ** 2
    return erreur ** 0.5

def erreur_Linf(data_instance, results, tableau_f):
    """
    Fonction permettant de calculer l'erreur Linf.

    Parameters
    ----------
    data_instance : TYPE class
        DESCRIPTION.
    results : TYPE tableau numpy
        DESCRIPTION.
    tableau_f : TYPE tableau numpy
        DESCRIPTION.

    Returns
    -------
    erreur : float
        Erreur Linf calculée.

    """
    erreur = [-1 * (results[-1][i] - tableau_f[i]) for i in range(data_instance.N)]
    return max(erreur)
