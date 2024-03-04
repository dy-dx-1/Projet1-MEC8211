import matplotlib.pyplot as plt 
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

def graphique_erreur(titre,x_values, y_values):
    """
    Affiche un graphique de l'évolution de l'erreur en fonction de dr.

    Parameters
    ----------
    titre : ordre de la soltuion
        
    x_values : list
        Liste des valeurs de dr.
    y_values : list of lists
        Liste des erreurs L1, L2, et Linf.

    Returns
    -------
    None
    """
    title='Evolution des erreurs L1, L2 et Linf en fonction de dr '+ titre
    x_dr=[0.5/(x_values[i]-1) for i in range(len(x_values))]
    plt.grid(True)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('dr')
    plt.ylabel('Erreurs')
    plt.title(title)

    for i in range(3):
        if i != 2:
            plt.plot(x_dr, y_values[i],linestyle='-', marker='o', label=f'Erreur L{i+1}')
        else:
            plt.plot(x_dr, y_values[i],linestyle='-', marker='o', label='Erreur Linf')
    
    plt.legend()
    plt.savefig(f'../results/{title.strip().lower().replace(" ", "")}', bbox_inches='tight')
    plt.show()
    
    """
    Code tiré du fichier de monsieur Vidal Graphique de convergence.py
    """
    
    
    # Ajuster une loi de puissance à toutes les valeurs (en utilisant np.polyfit avec logarithmes)
    i=0
    for error_values in y_values:
        
        if i != 2:
           nom_erreur=f'L{i+1}'
        else:
           nom_erreur='$L_{inf}$'

        # PRENONS LES 3 DERNIERS DR (LES PLUS PETITS)
        coefficients = np.polyfit(np.log(x_dr[-3:]), np.log(error_values[-3:]), 1)
        exponent = coefficients[0]
    
        # Fonction de régression en termes de logarithmes
        fit_function_log = lambda x: exponent * x + coefficients[1]
    
        # Fonction de régression en termes originaux
        fit_function = lambda x: np.exp(fit_function_log(np.log(x)))
    
        # Extrapoler la valeur prédite pour la dernière valeur de h_values
        #extrapolated_value = fit_function(x_dr[-1])
        
        # Tracer le graphique en échelle log-log avec des points et la courbe de régression extrapolée
        plt.figure(figsize=(8, 6))
        plt.scatter(x_dr, error_values, marker='o', color='b', label='Données numériques obtenues')
        plt.plot(x_dr, fit_function(x_dr), linestyle='--', color='r', label='Régression en loi de puissance')
        # Ajouter des étiquettes et un titre au graphique
              
        
        title='Convergence de l\'erreur' + nom_erreur +' en fonction de $Δx $'+titre
        
        
        plt.title(title,
                  fontsize=14, fontweight='bold', y=1.02)  # Le paramètre y règle la position verticale du titre
        
        plt.xlabel('Taille de maille $Δr$ (cm)', fontsize=12, fontweight='bold') 
        plt.ylabel('Erreur' + nom_erreur + ' (m/s)', fontsize=12, fontweight='bold')
        
        # Rendre les axes plus gras
        plt.gca().spines['bottom'].set_linewidth(2)
        plt.gca().spines['left'].set_linewidth(2)
        plt.gca().spines['right'].set_linewidth(2)
        plt.gca().spines['top'].set_linewidth(2)
        
        # Placer les marques de coche à l'intérieur et les rendre un peu plus longues
        plt.tick_params(width=2, which='both', direction='in', top=True, right=True, length=6)
        
        # Afficher l'équation de la régression en loi de puissance
        if i != 2:
            equation_text = nom_erreur + f'= {np.exp(coefficients[1])[0]:.4f} * Δx^({exponent[0]:.4f})'
        else: 
            equation_text = nom_erreur + f'= {np.exp(coefficients[1]):.4f} * Δx^({exponent:.4f})'
        equation_text_obj = plt.text(0.05, 0.05, equation_text, fontsize=12, transform=plt.gca().transAxes, color='k')
        
        # Déplacer la zone de texte
        equation_text_obj.set_position((0.5, 0.4))
        
        
        # Afficher le graphique
        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True)
        plt.legend()
        plt.savefig('../results/Erreur_de_Convergence_'+titre +'_'+ nom_erreur)
        
        plt.show()
        i+=1
        
    