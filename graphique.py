# -*- coding: utf-8 -*-
"""
Created on Thu Feb 1 11:59:25 2024

@author: alsip
"""
import numpy as np
import matplotlib.pyplot as plt
from analytique import analytique_sur_domaine

def graphique(data_instance, results):
    """
    Fonction pour générer un graphique de la solution analytique et numérique.

    Parameters
    ----------
    data_instance : Data
        Instance de la classe Data.
    results : numpy array
        Résultats de la solution numérique.

    Returns
    -------
    donne_Y : numpy array
        Solution analytique.

    """
    plt.figure(1)
    donne_X = [i * data_instance.dr for i in range(data_instance.Ntt)]
    donne_Y = analytique_sur_domaine(data_instance, donne_X)
    
    plt.plot(donne_X, donne_Y, label='Solution analytique')
    plt.plot(donne_X, results[-1], label='Solution numérique')
    
    plt.grid(True)
    plt.xlabel('Rayon en m')
    plt.ylabel('Concentration')
    plt.title(f'Evolution de la concentration de sel dans le pillier - {data_instance.Ntt}')
    plt.legend()
    plt.show()
    
    return donne_Y
