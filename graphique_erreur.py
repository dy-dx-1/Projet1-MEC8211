# -*- coding: utf-8 -*-
"""
Created on Thu Feb 1 13:52:53 2024

@author: alsip
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

def graphique_erreur(data_instance, x_values, y_values):
    """
    Affiche un graphique de l'évolution de l'erreur en fonction de dr.

    Parameters
    ----------
    data_instance : instance de la classe Data
        Instance contenant les données du problème.
    x_values : list
        Liste des valeurs de dr.
    y_values : list of lists
        Liste des erreurs L1, L2, et Linf.

    Returns
    -------
    None
    """
    plt.grid(True)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('dr')
    plt.ylabel('Erreur')
    plt.title('Evolution de l erreur L1, L2 et Linf en fonction de dr')

    for i in range(1, 4):
        y = y_values[i - 1]

        if i != 3:
            plt.plot(x_values, y, label=f'Erreur L{i}')
        else:
            plt.plot(x_values, y, label='Erreur Linf')

    plt.legend()
    plt.show()