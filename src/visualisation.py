import matplotlib.pyplot as plt 
import matplotlib.gridspec as gr
import numpy as np 

"""
Fichier regroupant les fonctions servant à la génération de graphiques. 
"""

def generate_n_graphs(params:object, solver_function, n_values:list)->list:
    """ 
    Fonction qui prend la fonction lambda d'un solveur ainsi qu'une liste de points à utiliser N 
    et génére une liste de résultats compatibles avec la fonction show_graphs. 

    Parameters
    ----------
    params: paramètres de la simulation
    solver function: fonction résolvant le profil de concentration 
    n_values: liste du nombre de noeuds à faire varier 
 
    Returns 
    ----------
    liste de tuples sous format [(domaine, image, label)]
    """
    graphiques = [] 
    for noeuds in n_values:  # génération de résultats pour différents types de noeuds
        params.N = noeuds
        params.domaine = np.linspace(0, params.ro, noeuds)
        profil_S_constant = solver_function() 
        graphiques.append((params.domaine, profil_S_constant, f"Numérique, N = {params.N}", ".-"))
    return graphiques 

def generate_dt_graphs(params:object, solver_function, dt_values:list)->list:
    """ 
    Équivalent de generate_n_graphs mais fait varier dt 
 
    Returns 
    ----------
    liste de tuples sous format [(domaine, image, label)]
    """
    graphiques = [] 
    for dt in dt_values:  # génération de résultats pour différents types de noeuds
        profil_S_constant = solver_function(dt) 
        graphiques.append((params.domaine, profil_S_constant, f"Numérique, dt = {dt}", ".-"))
    return graphiques 

def show_graphs(title:str, xaxis:str, yaxis:str, value_pairs:list):
    """
    Fonction permettant de générer et formatter facilement plusieurs graphiques avec des axes standard.

    Parameters
    ----------
    title: title of the graph
    xaxis: label for the x axis 
    yaxis: label for the y axis 
    value_pairs: list of tuples (dom, img, label, linestyle)

    Returns 
    ----------
    None 
    """
    for plot in value_pairs: 
        dom = plot[0]
        img = plot[1]
        text = plot[2]
        style = plot[3]
        plt.plot(dom, img,  style, label=text)
    
    plt.grid(True)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.title(title)
    plt.legend()
    plt.savefig(f'../results/{title.strip().lower().replace(" ", "")}', bbox_inches='tight')
    plt.show()
        
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
        print(f"{delta_vals[-3:] = }")
        print(f"{erreur[-3:] = }")
        coeffs = np.polyfit(np.log(delta_vals[-3:]), np.log(erreur[-3:]), 1)
        ordre = coeffs[0] if j=='inf' else coeffs[0][0] 
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
        plt.savefig(f'../results/MMS_{str(type_delta).upper()}/mms_err_L{j}_{type_delta}')
        plt.show()         