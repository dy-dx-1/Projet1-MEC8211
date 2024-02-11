import matplotlib.pyplot as plt 
import numpy as np 

def generate_n_graphs(params:object, solver_function, n_values:list)->list:
    """ 
    Fonction qui prend la fonction lambda d'un solveur ainsi qu'une liste de points à utiliser N 
    et génére une liste de résultats compatibles avec la fonction show_graphs. 
    """
    graphiques = [] 
    for noeuds in n_values:  # génération de résultats pour différents types de noeuds
        params.N = noeuds
        params.domaine = np.linspace(0, params.ro, noeuds)
        profil_S_constant = solver_function() 
        graphiques.append((params.domaine, profil_S_constant, f"Numérique, N = {params.N}", ".-"))
    return graphiques 

def show_graphs(title:str, xaxis:str, yaxis:str, value_pairs:list):
    """
    Fonction permettant de générer et formatter facilement plusieurs graphiques avec des axes standard.

    Parameters
    ----------
    value_pairs: list of tuples (dom, img, label, linestyle)
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