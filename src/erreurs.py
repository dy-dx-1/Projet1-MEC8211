# -*- coding: utf-8 -*-
"""
Fichier regroupant les fonctions de calcul d'erreur. 
"""
def erreur_L1(domaine, results_numerique, results_analytique):
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
    for i in range(len(domaine)):
        erreur += abs(results_numerique[i] - results_analytique[i])
    return erreur/len(domaine)

def erreur_L2(domaine, results_numerique, results_analytique):
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
    for i in range(len(domaine)):
        erreur += (results_numerique[i] - results_analytique[i]) ** 2
    return (erreur/len(domaine)) ** 0.5

def erreur_Linf(domaine, results_numerique, results_analytique):
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
    erreur = abs(results_numerique - results_analytique)
    return max(erreur)
