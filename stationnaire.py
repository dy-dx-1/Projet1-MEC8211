import numpy as np; np.set_printoptions(precision=2, linewidth=150) # permet d'imprimer les arrays de manière plus compacte pr les inspecter 
import matplotlib.pyplot as plt 

class Data: # défini les paramètres du problème  
    ro = 0.5  # Diamètre du cylindre [m]
    D = 10**(-10) # coeff diffusion effective 
    S = 8*(10**(-9)) # terme source si constant 
    k = 4*(10**(-9)) # constante de réaction si réaction du premier ordre 
    C_ext = 12 # Concentration à l'extérieur 

    N = 5 
    domaine = np.linspace(0, ro, N)

def solveur_stationnaire(data, consommation_constante:bool, ordre_disc_neumann:int): 
    """
    Résout la diffusion dans le pilier dans le régime permanent. 

    data: obj contenant les paramètres suivants:
        [...]
    N: nombre de points de discrétisation du domaine 
    ordre_disc_neumann: Ordre de la discrétisation spatiale au noeud 0, peut être 1 ou 2 
    """
    ro, D, S, k, C_ext, N, domaine = data.ro, data.D, data.S, data.k, data.C_ext, data.N, data.domaine
    dr = ro/(N-1)   # pas de discrétisation spatiale 

    ## Initialisation des matrices 
    A = np.zeros((N, N))
    B = np.zeros((N, 1))

    ## Remplissage du centre
    if consommation_constante: # remplissage du centre diffère selon consommation constante ou premier ordre 
        # Coefficients associés aux noeuds 
        alpha = lambda ri: np.true_divide(-D, np.square(dr)) - np.true_divide(D, dr*ri) # ci+1
        beta = lambda ri: np.true_divide(2*D, dr**2) + np.true_divide(D, ri*dr)         # ci 
        zeta = np.true_divide(-D, dr**2)                                                # ci-1
        for i in range(1, N-1): # descente verticale (sur les lignes)
            r = domaine[i]
            A[i, i+1] = alpha(r)
            A[i, i] = beta(r) 
            A[i, i-1] = zeta 
            B[i, 0] = - S 
    else: 
        pass 

    ## Ajout des conditions limites 
    # Neumann 
    if ordre_disc_neumann==1: # Dérivation avant ordre 1 
        A[0, 0] = -1 
        A[0, 1] = 1 
    elif ordre_disc_neumann==2: # Dérivation gear avant 
        A[0, 0] = -3 
        A[0, 1] = 4
        A[0, 2] = -1 
    else: # pas supporté 
        print("Ordre de disc pour Neumann autre que 1 ou 2 non supporté")
        return None  
    B[0, 0] = 0 
    # Dirichlet 
    A[N-1, N-1] = 1 
    B[N-1, 0] = C_ext 

    ## Solution du système 
    C = np.linalg.solve(A, B)[:,0] # Retour sous la forme [C0, C1, ..., CN]
    return C

def main():
    d = Data() 
    domaine = d.domaine
    C = solveur_stationnaire(d, True, 1)
    print(C) 
    # Affichage 
    plt.plot(domaine, C, ".-") 
    C_exact = np.true_divide(d.S,4*d.D)*np.square(d.ro)*(np.square(np.divide(d.domaine, d.ro))-1)+d.C_ext
    plt.plot(domaine, C_exact) # analytique 
    plt.show() 
              

if __name__ == "__main__":
    main() 