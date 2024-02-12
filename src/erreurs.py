# -*- coding: utf-8 -*-
from math import log
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

def erreur_de_convergence_observe(params,n_values,Erreur_L1,Erreur_L2,Erreur_Linf):
    x_dr=[params.ro/(n_values[i]-1) for i in range(len(n_values))]
    print("Ordre de convergence observé")
    print("Erreur L1 " + str(log(Erreur_L1[0]/Erreur_L1[2])/log(x_dr[0]/x_dr[2])))
    print("Erreur L2 " +str((log(Erreur_L2[0]/Erreur_L2[2])/log(x_dr[0]/x_dr[2]))))
    print("Erreur Linf " +str((log(Erreur_Linf[0]/Erreur_Linf[2])/log(x_dr[0]/x_dr[2]))))
    ### Question F: Profils avec différentiation ordre 2 