import matplotlib.pyplot as plt 

def graphique(title:str, xaxis:str, yaxis:str, *value_pairs):
    """
    Fonction permettant de générer et formatter facilement plusieurs graphiques avec des axes standard.

    Parameters
    ----------
    value_pairs: tuples (dom, img, label, linestyle)
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