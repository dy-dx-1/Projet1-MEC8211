import matplotlib.pyplot as plt 
import matplotlib.gridspec as gr
import numpy as np 
from math import log

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
        for j in range(len(domaine)):
            erreur += abs(results_numerique[i][j] - results_analytique[i][j])
    return erreur/(len(domaine)**2)

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
        for j in range(len(domaine)):
            erreur += (results_numerique[i][j] - results_analytique[i][j]) ** 2
    return (erreur/len(domaine)**2) ** 0.5

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
    erreur = np.average(abs(results_numerique - results_analytique)) # car results numérique est sous forme colonne et analytique sous forme ligne 
    return np.amax(erreur)

def graphique_convergence_erreurs(delta_vals:list, erreurs:list, type_delta:str):
    """
    Affiche un graphique de l'évolution de l'erreur en fonction de dt ou de dr.

    Parameters
    ----------        
    delta_vals : list
        Liste des valeurs de dt ou dr.
    erreurs : list of lists
        Liste des erreurs L1, L2, et Linf.
    type_delta : 'dt' ou 'dr' 

    Returns
    -------
    None
    """
    print(f"***Ordre de convergence {'SPATIAL' if type_delta=='dr' else 'TEMPOREL'} observé***")
    for i, erreur in enumerate(erreurs): 
        j = 'inf' if i==2 else str(i+1) 
        coeffs = np.polyfit(np.log(delta_vals[-3:]), np.log(erreur[-3:]), 1)

        ordre = coeffs[0] if j=='inf' else coeffs[0]
        print(f"Erreur L{j} : {ordre:.4f}")

        fit_function_log = lambda x: ordre * x + coeffs[1]
        # Fonction de régression en termes originaux
        fit_function = lambda x: np.exp(fit_function_log(np.log(x)))
        plt.scatter(delta_vals, erreur, marker='o', color='b', label=f"Erreur L{j} ; Ordre: {ordre:.4f}")
        plt.plot(delta_vals, fit_function(delta_vals), linestyle='--', color='r', label='Régression en loi de puissance')
       
        plt.legend() 
        plt.grid(True)
        plt.yscale('log')
        plt.xscale('log')
        if type_delta=="dr":
            plt.ylabel('Erreur ')
            plt.xlabel('dr [m]')
            plt.title(f"Convergence de l'erreur L{j} selon le pas spatial")
        elif type_delta=="dt":
            plt.ylabel('Erreur ')
            plt.xlabel('dt [s]')
            plt.title(f"Convergence de l'erreur L{j} selon le pas de temps")
        else:
            print("type delta in graphique_convergence_erreurs not valid")
            return 
        plt.savefig(f'Convergence_de_l-erreur_L{j}.png')
        plt.show() 