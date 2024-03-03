import numpy as np; np.set_printoptions(precision=2, linewidth=150) # permet d'imprimer les arrays de manière plus compacte pr les inspecter 

"""
Fichier regroupant les méthodes numériques 
"""

def solveur_stationnaire(data:object, consommation_constante:bool, ordre_derive_premiere:int): 
    """
    Résout la diffusion dans le pilier dans le régime permanent. 

    
    Parameters
    ----------
    data: objet contenant les paramètres de simulation 
    consommation_constante: bool indiquant si la source de concentration est constante ou non (d'ordre 1)
    ordre_derive_premiere: Ordre de la discrétisation spatiale des dérivées premieres qui ne sont pas au bord 
    
    Returns
    ----------
    Array 1D [1xNoeuds] du profil de concentration dans la poutre 
    """
    ro, D, S, k, C_ext, N, domaine = data.ro, data.D, data.S, data.k, data.C_ext, data.N, data.domaine
    dr = ro/(N-1)   # pas de discrétisation spatiale 

    # Coefficients associés aux noeuds 
    if ordre_derive_premiere==1: # approx d'ordre 1 pas avant 
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

    ## Initialisation des matrices 
    A = np.zeros((N, N))
    B = np.zeros((N, 1))

    ## Remplissage du centre 
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
    """
    Résout la diffusion dans le pilier dans le régime transitoire à l'aide d'un schéma Euler implicite. 
    
    Parameters
    ----------
    data: objet contenant les paramètres de simulation 
    consommation_constante: bool indiquant si la source de concentration est constante ou non (d'ordre 1)
    ordre_derive_premiere: Ordre de la discrétisation spatiale des dérivées premieres qui ne sont pas au bord 
    
    Returns
    ----------
    Array 1D [1xNoeuds] du profil de concentration dans la poutre 
    """
    ## Setup params situation
    ro, D, S, k, C_ext, N, domaine = data.ro, data.D, data.S, data.k, data.C_ext, data.N, data.domaine
    dr = ro/(N-1)   # pas de discrétisation spatiale 

    dt = 1e5
    t = 0 # temps initial 
    nb_annees = 100
    nb_jours = nb_annees*365.25
    t_sim = int(nb_jours*24*60*60) # temps de simulation 
    print(f"Simulation transitoire lancée avec {N=}noeuds ; {dt=}s ; pendant {nb_annees=} annees")

    ## Coefficients associés aux noeuds 
    if ordre_derive_premiere==1: # approx d'ordre 1 pas avant 
        # Coefficients associés aux noeuds 
        alpha = lambda ri: np.true_divide(D, np.square(dr)) + np.true_divide(D, dr*ri) # ci+1
        beta_ = lambda ri: -np.true_divide(1, dt)-np.true_divide(2*D, dr**2) - np.true_divide(D, ri*dr)       # ci, _ car il sera encore modifie selon S 
        zeta = lambda ri: np.true_divide(D, dr**2)                                                # ci-1   
    elif ordre_derive_premiere==2: # approx d'ordre 2 centrée 
        alpha = lambda ri: np.true_divide(D, np.square(dr)) + np.true_divide(D, 2*dr*ri) # ci+1
        beta_ = lambda ri: np.true_divide(-2*D, dr**2)-np.true_divide(1, dt)            # ci, _ car il sera encore modifie selon S 
        zeta = lambda ri: np.true_divide(D, dr**2) - np.true_divide(D, 2*dr*ri)    # ci-1  
    else: # pas supporté 
        print("Ordre de disc derive premiere autre que 1 ou 2 non supporté")
        return None  
    
    if consommation_constante: # affecte le membre de droite et beta 
        coeff_droite = lambda Ci_t: S - np.true_divide(Ci_t, dt)
        beta = beta_ 
    else: 
        coeff_droite = lambda Ci_t: -np.true_divide(Ci_t, dt)
        beta = lambda ri: beta_(ri)-k 

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
            A[i, i-1] = zeta(r)
            B[i, 0] = coeff_droite(C[i]) # le C indexé correspond au C au temps t, vu qu'on calcule pour le t+1 
        ### Ajout des conditions limites 
        ## Neumann 
        A[0, 0] = -3 
        A[0, 1] = 4
        A[0, 2] = -1 
        B[0, 0] = 0 
        ## Dirichlet 
        A[N-1, N-1] = 1 
        B[N-1, 0] = C_ext 
        
        ### Solution du système 
        C_new = np.linalg.solve(A, B) # nouvelles valeurs donc on peut passer à la prochaine itération 
        C =np.copy(C_new)
        t+=dt
    return C 

def solveur_MMS(data:object, consommation_constante:bool, ordre_derive_premiere:int): 
    """
    Résout la diffusion dans le pilier dans le régime transitoire à l'aide d'un schéma Euler implicite. 
    
    Parameters
    ----------
    data: objet contenant les paramètres de simulation 
    consommation_constante: bool indiquant si la source de concentration est constante ou non (d'ordre 1)
    ordre_derive_premiere: Ordre de la discrétisation spatiale des dérivées premieres qui ne sont pas au bord 
    
    Returns
    ----------
    Array 1D [1xNoeuds] du profil de concentration dans la poutre 
    """
    ## Setup params situation
    ro, D, S, k, C_ext, N, domaine = data.ro, data.D, data.S, data.k, data.C_ext, data.N, data.domaine
    dr = ro/(N-1)   # pas de discrétisation spatiale 
    print(S)
    dt = 1e5
    t = 0 # temps initial 
    nb_annees = 100
    nb_jours = nb_annees*365.25
    t_sim = int(nb_jours*24*60*60) # temps de simulation 
    print(f"Simulation transitoire lancée avec {N=}noeuds ; {dt=}s ; pendant {nb_annees=} annees")

    ## Coefficients associés aux noeuds 
    if ordre_derive_premiere==1: # approx d'ordre 1 pas avant 
        # Coefficients associés aux noeuds 
        alpha = lambda ri: np.true_divide(D, np.square(dr)) + np.true_divide(D, dr*ri) # ci+1
        beta_ = lambda ri: -np.true_divide(1, dt)-np.true_divide(2*D, dr**2) - np.true_divide(D, ri*dr)       # ci, _ car il sera encore modifie selon S 
        zeta = lambda ri: np.true_divide(D, dr**2)                                                # ci-1   
    elif ordre_derive_premiere==2: # approx d'ordre 2 centrée 
        alpha = lambda ri: np.true_divide(D, np.square(dr)) + np.true_divide(D, 2*dr*ri) # ci+1
        beta_ = lambda ri: np.true_divide(-2*D, dr**2)-np.true_divide(1, dt)              # ci, _ car il sera encore modifie selon S 
        zeta = lambda ri: np.true_divide(D, dr**2) - np.true_divide(D, 2*dr*ri)    # ci-1  
    else: # pas supporté 
        print("Ordre de disc derive premiere autre que 1 ou 2 non supporté")
        return None  
    
    if consommation_constante: # affecte le membre de droite et beta 
        coeff_droite = lambda Ci_t: S - np.true_divide(Ci_t, dt)
        beta = beta_ 
        # n'intervien plus
    else: 
        coeff_droite = lambda Ci_t,r,t: -np.true_divide(Ci_t, dt) - S(r,t)
        beta = beta_ 

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
            A[i, i-1] = zeta(r)
            B[i, 0] = coeff_droite(C[i],r,t) # le C indexé correspond au C au temps t, vu qu'on calcule pour le t+1 
        ### Ajout des conditions limites 
        ## Neumann 
        A[0, 0] = -3 
        A[0, 1] = 4
        A[0, 2] = -1 
        B[0, 0] = 0 
        ## Dirichlet 
        A[N-1, N-1] = 1 
        B[N-1, 0] = C_ext 
        
        ### Solution du système 
        C_new = np.linalg.solve(A, B) # nouvelles valeurs donc on peut passer à la prochaine itération 
        C =np.copy(C_new)
        t+=dt
    return C 