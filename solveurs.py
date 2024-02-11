"""
Fichier regroupant les méthodes numériques 
"""
import numpy as np; np.set_printoptions(precision=2, linewidth=150) # permet d'imprimer les arrays de manière plus compacte pr les inspecter 

def solveur_stationnaire(data:object, consommation_constante:bool, ordre_derive_premiere:int): 
    """
    Résout la diffusion dans le pilier dans le régime permanent. 

    data: obj contenant les paramètres suivants:
        [...]
    N: nombre de points de discrétisation du domaine 
    ordre_derive_premiere: Ordre de la discrétisation spatiale des dérivées premieres qui ne sont pas au bord 
    """
    ro, D, S, k, C_ext, N, domaine = data.ro, data.D, data.S, data.k, data.C_ext, data.N, data.domaine
    dr = ro/(N-1)   # pas de discrétisation spatiale 

    ## Initialisation des matrices 
    A = np.zeros((N, N))
    B = np.zeros((N, 1))

    ## Remplissage du centre
    if ordre_derive_premiere==1: # approx d'ordre 1 pas avant 
        # Coefficients associés aux noeuds 
        alpha = lambda ri: np.true_divide(D, np.square(dr)) + np.true_divide(D, dr*ri) # ci+1
        beta_ = lambda ri: np.true_divide(-2*D, dr**2) - np.true_divide(D, ri*dr)       # ci, _ car il sera encore modifie selon S 
        zeta = lambda ri: np.true_divide(D, dr**2)                                                # ci-1   
    elif ordre_derive_premiere==2: # approx d'ordre 2 centrée 
        alpha = lambda ri: np.true_divide(D, np.square(dr)) + np.true_divide(D, 2*dr*ri) # ci+1
        beta_ = lambda ri: np.true_divide(-2*D, dr**2)            # ci, _ car il sera encore modifie selon S 
        zeta = lambda ri: np.true_divide(D, dr**2) - np.true_divide(D, 2*dr*ri)    # ci-1  
    else: # pas supporté 
        print("Ordre de disc derive premiere autre que 1 ou 2 non supporté")
        return None  
    
    if consommation_constante: # affecte le membre de droite et beta 
        coeff_droite = S
        beta = beta_ 
    else: 
        coeff_droite = 0
        beta = lambda ri: beta_(ri)-k 

    for i in range(1, N-1): # descente verticale (sur les lignes)
        r = domaine[i]
        A[i, i+1] = alpha(r)
        A[i, i] = beta(r) 
        A[i, i-1] = zeta(r) 
        B[i, 0] = coeff_droite 

    ## Ajout des conditions limites 
    # Neumann 
    A[0, 0] = -3 
    A[0, 1] = 4
    A[0, 2] = -1 
    B[0, 0] = 0 
    # Dirichlet 
    A[N-1, N-1] = 1 
    B[N-1, 0] = C_ext 

    ## Solution du système 
    C = np.linalg.solve(A, B)[:,0] # Retour sous la forme [C0, C1, ..., CN]
    return C

def solveur_transitoire(data:object, consommation_constante:bool, ordre_derive_premiere:int): 
    ## Setup params situation
    ro, D, S, k, C_ext, N, domaine = data.ro, data.D, data.S, data.k, data.C_ext, data.N, data.domaine
    dr = ro/(N-1)   # pas de discrétisation spatiale 

    dt = 500
    t = 0 # temps initial 
    nb_jours = 1000
    t_sim = nb_jours*60*60*24 # temps de simulation 

    ## Coefficients associés aux noeuds 
    alpha = lambda ri: np.true_divide(-D, np.square(dr)) - np.true_divide(D, dr*ri) # ci+1
    beta = lambda ri: np.true_divide(1,dt) + np.true_divide(2*D, dr**2) + np.true_divide(D, ri*dr)
    zeta = np.true_divide(-D, dr**2)

    ### conditions initiales 
    C = np.zeros(N) 
    Ci = 0 
    for i in range(N): 
        C[i]=Ci 
    while t<=t_sim: 
        A = np.zeros((N, N))
        B = np.zeros((N, 1))
        ### Construction centre de la matrice 
        for i in range(1, N-1): # descente verticale (sur les lignes)
            r = domaine[i]
            A[i, i+1] = alpha(r)
            A[i, i] = beta(r) 
            A[i, i-1] = zeta 
            B[i, 0] = np.true_divide(C[i], dt) - S # le C indexé correspond au C au temps t, vu qu'on calcule pour le t+1 
        ### Ajout des conditions limites 
        ## Neumann 
        A[0, 0] = -1 
        A[0, 1] = 1 ## mntn derivee avant ordre 1 
        B[0, 0] = 0 
        ## Dirichlet 
        A[N-1, N-1] = 1 
        B[N-1, 0] = C_ext 
        ### Solution du système 
        C_new = np.linalg.solve(A, B) # nouvelles valeurs donc on peut passer à la prochaine itération 
        C =np.copy(C_new)
        t+=dt
    return C 