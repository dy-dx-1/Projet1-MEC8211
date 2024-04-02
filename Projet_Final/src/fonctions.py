import numpy as np 
import pytest

np.set_printoptions(precision=2, linewidth=150) # permet d'imprimer les arrays de manière plus compacte pr les inspecter 

def psi_exact(r:float, theta:float, params:object)->float:
    """
    Évalue la solution analytique de l'equation de Laplace en coordonées polaires. 

    Entrées: 
    r : Coordonée radiale [m] 
    theta : Coordonée angulaire [rad] 
    params: Objet contenant les paramètres de la situation 

    Sorties: 
    La valeur de la fonction de courant Psi [m^2/s]
    """ 
    return params.u_inf * r * np.sin(theta)*(1-np.square(params.R/r))

def delpsi_delr_ref(r:float, theta:float, params:object)->float: 
    """ 
    Évalue la dérivée partielle de psi par rapport à r de façon analytique, sert à vérifier calculs de vitesse  

    Entrées: 
    r : Coordonée radiale [m] 
    theta : Coordonée angulaire [rad] 
    params: Objet contenant les paramètres de la situation 

    Sorties: 
    La valeur de la fonction de courant Psi dérivée par rapport à r [m/s]
    """
    return params.u_inf*np.sin(theta)*(np.square(r)+np.square(params.R))/np.square(r)

def delpsi_deltheta_ref(r:float, theta:float, params:object)->float: 
    """ 
    Évalue la dérivée partielle de psi par rapport à theta de façon analytique, sert à vérifier calculs de vitesse  

    Entrées: 
    r : Coordonée radiale [m] 
    theta : Coordonée angulaire [rad] 
    params: Objet contenant les paramètres de la situation 

    Sorties: 
    La valeur de la fonction de courant Psi dérivée par rapport à theta [m^2/s]  
    """
    return params.u_inf*(np.square(r)-np.square(params.R))*np.cos(theta)/r 

def psi_ref_mesh(prm:object)->np.ndarray:
    """ 
    Applique la solution analytique de la fonction de courant sur le maillage établi par les paramètres de notre situation. 

    Entrées: 
    prm: Objet contenant les paramètres de la situation 

    Sorties:
    ndarray bidimensionnel représentant les valeurs de Psi analytique sur le maillage de notre situation. 
    """
    maille_r, maille_theta = gen_maille(prm.R, prm.R_ext, prm.theta_min, prm.theta_max, prm.nx, prm.ny) # sert à retourver coords dans notre maillage 
    return np.array(psi_exact(maille_r, maille_theta, prm)) 

def vr_ref_mesh(prm:object)->np.ndarray: 
    """ 
    Applique la solution analytique de la dérivée partielle par rapport à theta de la fonction de courant
    sur le maillage établi par les paramètres de notre situation afin de trouver le maillage de vitesses radiales. 

    Entrées: 
    prm: Objet contenant les paramètres de la situation 

    Sorties:
    ndarray bidimensionnel représentant les valeurs de vr = (1/r)*(∂Ψ/∂θ) analytique sur le maillage de notre situation. 
    """
    maille_r, maille_theta = gen_maille(prm.R, prm.R_ext, prm.theta_min, prm.theta_max, prm.nx, prm.ny) # sert à retourver coords dans notre maillage 
    return np.array((1/maille_r)*delpsi_deltheta_ref(maille_r, maille_theta, prm)) 

def vtheta_ref_mesh(prm:object)->np.ndarray: 
    """ 
    Applique la solution analytique de la dérivée partielle par rapport à r de la fonction de courant
    sur le maillage établi par les paramètres de notre situation afin de trouver le maillage de vitesses angulaires. 

    Entrées: 
    prm: Objet contenant les paramètres de la situation 

    Sorties:
    ndarray bidimensionnel représentant les valeurs de vtheta = (-1)*(∂Ψ/∂r) analytique sur le maillage de notre situation. 
    """
    maille_r, maille_theta = gen_maille(prm.R, prm.R_ext, prm.theta_min, prm.theta_max, prm.nx, prm.ny) # sert à retourver coords dans notre maillage 
    return np.array(-delpsi_delr_ref(maille_r, maille_theta, prm)) 

def gen_maille(r_min:float, r_max:float, theta_min:float, theta_max:float, nx:int, ny:int)->'tuple[np.ndarray, np.ndarray]': 
    """ 
    Genère les coordonnées r et theta d'un maillage allant de r_min->r_max de gauche à droite et de theta_min->theta_max de bas en haut

    Entrées: 
    r_min: Position radiale minimum 
    r_max: Position radiale maximum 
    theta_min: Position angulaire minimum 
    theta_max: Position angulaire maximum 
    nx: Nombre de noeuds sur l'horizontale du maillage (axe radial) 
    ny: Nombre de noeuds sur la verticale du maillage (axe angulaire) 

    Sorties: 
    tuple contenant deux ndarrays bidimensionnels, l'un représentant les coordonées radiales à chaque noeud et l'autre les coordonées angulaires 
    """
    maille_r = np.array([ [r for r in np.linspace(r_min, r_max, nx)] for _ in range(ny) ])
    maille_theta =  np.array([ [theta for _ in range(nx)] for theta in np.linspace(theta_max, theta_min, ny) ])
    return maille_r, maille_theta

def convert_indices(nx:int, i:'int|None' = None, j:'int|None' = None, k:'int|None' = None)->int: 
    """
    Prend 2 indices et retourne celui qui n'est pas spécifié selon un maillage de forme 

     i =0   j=1    j=2    ... j=nx-1
    [[k=0   k=1    k=2    ... k=nx-1 ],     j=0
     [k=nx  k=nx+1 k=nx+2 ... k=2nx-1],     j=1
     [...   ...    ...    ... ...    ],     ...
     [...   ...    ...    ... k = N-1] ]    j = ny-1 

    Entrées: 
    nx: Nombre de noeuds sur l'axe horizontal 
    Et 2 des index parmi les suivants, 
    i: Index 1d horizontal du noeud tel que i ∈ [0, nx-1]
    j: Index 1d vertical du noeud tel que j ∈ [0, ny-1]
    k: Index 1d du noeud tel que k ∈ [0, N-1] ; N = nx*ny 
    
    Sorties: 
    L'index qui n'est pas spécifié (ou None) des entrées
    """
    # on assume que le programmeur sait utiliser la fonction donc pas de check complet des paramètres passés
    if i is None: 
        return int(k - (nx*j)) 
    elif j is None: 
        return int((k-i) / nx) 
    elif k is None: 
        return int(i + (j*nx)) 
    else: 
        return None 
    
def gen_central_values(k:int, nx:int, ny:int, rk:float, dr:float, dtheta:float)->np.ndarray: 
    """
    Génére les valeurs de noeuds centraux (qui ne sont pas sous l'effet des conditions limites) de la matrice des noeuds lors de la résolution 
    du système par la méthode des différences finies. Séparer ces calculs ici permet de rendre la fonction mdf() moins encombrée et faciliter les tests. 

    Entrées: 
    k: Index 1d du noeud tel que k ∈ [0, N-1] ; N = nx*ny 
    nx: Nombre de noeuds sur l'axe radial 
    ny: Nombre de noeuds sur l'axe angulaire 
    rk: Coordonée radiale associée au noeud k [m] 
    dr: Pas de différentiation radial [m] 
    dtheta: Pas de différentiation angulaire [rad] 

    Sorties: 
    ndarray bidimensionnel contenant la matrice des noeuds remplie avec la ligne associée au k rentré en paramètre, cet array sera ensuite sommé 
    à la matrice de noeuds complète dans la méthode mdf. 
    """
    N = nx*ny 
    # on crée un matrice NxN qu'on remplira des coefficients 
    # on sépare ceci de la matrice des noeuds de la fonction mdf pour faciliter nos tests, on devrait avoir une matrice dont toutes les valeurs des bords sont nulles 
    mat_ref = np.zeros((N, N))    
    Tk_nx = 1 / (np.square(rk)*np.square(dtheta)) 
    Tk_nx_ = Tk_nx
    Tk_1 = (1/np.square(dr)) + (1/(2*rk*dr))
    Tk_1_ = (1/np.square(dr)) - (1/(2*rk*dr)) 
    Tk = (-2/np.square(dr)) + (-2/(np.square(rk)*np.square(dtheta)))           

    # Plaçons les coefficients dans la matrice 
    mat_ref[k, k] = Tk 
    mat_ref[k, k+1] = Tk_1 
    mat_ref[k, k-1] = Tk_1_
    mat_ref[k, k+nx] = Tk_nx 
    mat_ref[k, k-nx] = Tk_nx_
    # Le résidu est nul pour ces noeuds dans cette situation donc on n'a pas besoin de le modifier  
    return mat_ref

def mdf(params:object)->'tuple[np.ndarray, np.ndarray, np.ndarray]': 
    """
    Applique la méthode des différences finies pour résoudre le système sur le domaine 2D du problème. 

    Entrées: 
    params: Objet contenant les paramètres du problème 

    Sorties: 
    Un tuple contenant les 3 éléments suivants, 
    maille_r: Maille bidimensionnelle (ndarray ny par nx) des coordonées radiales de notre situation 
    maille_theta: Maille bidimensionnelle (ndarray ny par nx) des coordonées angulaires de notre situation 
    solutions: Maille unidimensionnelle (ndarray 1 par N) des résultats de la fonction de courant Ψ de notre situation sur les noeuds k ∈ [0, N-1] 
    """
    nx, ny = params.nx, params.ny
    r_min, r_max, theta_min, theta_max = params.R, params.R_ext, params.theta_min, params.theta_max
    maille_r, maille_theta = gen_maille(r_min, r_max, theta_min, theta_max, nx, ny)
    dr = abs(r_max-r_min)/(nx-1)
    dtheta = abs(theta_max-theta_min)/(ny-1)
    # Matrice qui acceuillera les différentes solutions des noeuds 
    N = nx*ny 
    noeuds = np.zeros((N,N)) 
    # Vecteur résidu associé à la matrice des noeuds 
    res = np.zeros(N)
    # Itérons sur chacun des k afin de remplir la matrice des noeuds et du résidu 
    for k in range(N): 
        if k<=(nx-1): # Condition limite du haut ; Psik = 0 
            noeuds[k, k] = 1 # pas besoin de changer le résidu car 0 
        elif k>=(N-nx) and k<=(N-1): # Condition limite du bas ; Psik = 0 
            noeuds[k, k] = 1
        elif k%nx==0: # Condition limite de gauche ; Psik = 0 
            noeuds[k, k] = 1
        elif (k+1)%nx==0: # Condition limite de droite ; psik est une fonction 
            noeuds[k, k] = 1
            # calculons le résultat de la fonction qui ira dans le résidu 
            i = nx-1 # on est à droite 
            j = convert_indices(nx, i=i, j=None, k=k) 
            theta_k = maille_theta[j, i]
            res[k] = params.u_inf*r_max*np.sin(theta_k)*(1-np.square(r_min/r_max))
        else: # Alors on est à un noeud qui n'est pas sur le bord 
            # Trouvons le r associé à k 
            i = k%nx 
            j = convert_indices(nx, i=i, j=None, k=k)
            rk = maille_r[j, i]
            # Évaluons les coefficients des différents noeuds de T, soit Tk+nx, Tk-nx, Tk+1, Tk-1 
            noeuds += gen_central_values(k, nx, ny, rk, dr, dtheta)
    solutions = np.linalg.solve(noeuds, res)
    return maille_r, maille_theta, solutions  

def deriv_by_coeff(psis:np.array, coeff:str, nx:int, delta:float)->np.ndarray: 
    """ 
    Génére les dérivées numériques d'un array de valeurs aux noeuds. Cette fonction est utilisée par la fonction vitesses() pour évaluer les dérivées 
    des valeurs de Ψ selon r ou theta. Si c'est selon r, on dérive de gauche à droite donc les noeuds varient entre k-1 et k+1, alors que si c'est
    selon theta, on dérive de bas en haut donc les noeuds varient entre k-nx et k+nx. 

    Entrées: 
    psis: Maille unidimensionnelle (ndarray 1 par N) des résultats de la fonction de courant Ψ de notre situation sur les noeuds k ∈ [0, N-1]
    coeff: Coefficient indiquant la direction de la dérivée (soit "r" ou "theta") 
    nx: Nombre de noeuds sur l'axe radial 
    delta: Pas de différentiation associé au coefficient (donc soit la valeur de dr ou de dtheta)

    Sorties: 
    ndarray de la même forme et ordre que psis en entrée (1xN), mais dont les valeurs correspondent aux dérivées de ceux-ci selon la direction spécifiée
    """
    coeff = coeff.strip().lower() 
    N = len(psis)
    if not any([coeff=="r", coeff=="theta"]): return None # check rapide que la fonction est bien utilisée 
    psi_prime = list() # Liste qui contiendra les psi dérivés en ordre 
    for k, psi in enumerate(psis): 
        # Il faut savoir si on est sur l'axe des r ou de theta pour appliquer les bonnes conditions 
        # on appliquera ensuite les mêmes structures de contrôle que dans la mdf pour savoir si on est sur le perimetre et donc quelle derivee appliquer
        if coeff == "r": 
            # alors derivée 'horizontale' sur notre maillage, on a juste a vérifier si on est a gauche ou a droite 
            if k%nx==0: # gauche, derivee gear avant ordre 2 
                psi_p = -psis[k+2] + (4*psis[k+1]) - (3*psi)
            elif (k+1)%nx==0: # droite, derivee gear arriere ordre 2 
                psi_p = (3*psi) - (4*psis[k-1]) + psis[k-2]
            else: # milieu, derivee centree ordre 2 
                psi_p = psis[k+1]-psis[k-1]
        else: # notre verification initiale nous permet d'assurer que si ce n'Est pas r, c'est theta qu'on veut 
            # alors derivee 'verticale' sur le maillage, on a besoin de verifier si on est en haut ou bas 
            if k<=(nx-1): # haut, derivee gear avant ordre 2 
                psi_p = (-psis[k+nx+nx] + (4*psis[k+nx]) - (3*psi)) * -1
            elif k>=(N-nx) and k<=(N-1): # bas, derivee gear arriere ordre 2
                psi_p = ((3*psi) - (4*psis[k-nx]) + psis[k-nx-nx]) * -1 
            else: # centre, derivee centree ordre 2 
                psi_p = (psis[k+nx]-psis[k-nx]) * -1    
                # on ajoute des *-1 partout car en vertical k-nx est notre theta plus grand pour la maille qu'on a défini avec theta qui grandit de bas en haut
        psi_prime.append(psi_p/(2*delta))
    return np.array(psi_prime)

def vitesses(psi:np.ndarray, params:object)->'tuple[np.ndarray, np.ndarray]': 
    """
    Calcule les vitesses radiale et angulaires à partir des solutions discrètes de la fonction de courant.  
    
    Entrées: 
    psi: ndarray unidimensionnel de taille N noeuds, correspondant aux Ψ de ces noeuds 
    params: Objet contenant les paramètres du problème
    
    Sortie:
    Un tuple contenant, 
    vr: ndarray unidimensionnel de taille N noeuds, correspondant à la vitesse radiale de ces noeuds
    vtheta: ndarray unidimensionnel de taille N noeuds, correspondant à la vitesse angulaire de ces noeuds
    """
    nx = params.nx
    ny = params.ny 
    r = np.linspace(params.R, params.R_ext, nx) 

    dr = abs(params.R_ext-params.R)/(nx-1)
    dtheta = abs(params.theta_max-params.theta_min)/(ny-1)
    # Note: r est un vecteur 1d de longueur nx alors que le vect des derivees est 1d longueur N (parce que c'est des solutions aux nx*ny noeuds) 
    # on doit donc creer r_ qui represente les valeurs de r à chaque noeud dans l'ordre du vect des derivées pour pouvoir les multiplier 
    r_ = np.array(sum([list(r) for _ in range(ny)], [])) 
    vr = (1/r_)*deriv_by_coeff(psi, 'theta', nx, dtheta)
    vtheta = -deriv_by_coeff(psi, 'r', nx, dr)
    return vr, vtheta

def arrange_mesh(vector:np.ndarray, nx:int, ny:int)->np.ndarray: 
    """
    Prend un vecteur 1d correspondant à des valeurs associées à des noeuds K et les retourne en format 2D selon la maille nx*ny. 
    Par exemple, cette fonction peut prendre les solutions de psi de la fonction mdf() et les place sur la maille définie par notre problème

    Entrées: 
    vector: ndarray 1d des valeurs associées aux noeuds k du maillage 
    nx: Nombre de noeuds sur l'axe horizontal du maillage 
    ny: Nombre de noeuds sur l'axe vertical du maillage 

    Sorties: 
    ndarray 2d des valeurs de vector placées sur le maillage défini par nx et ny 
    """
    maille = []
    for k in range(0, nx*ny, nx): 
        maille.append(vector[k:k+nx])
    return np.array(maille)

def convert_coords(maille_r:np.ndarray, maille_theta:np.ndarray, maille_vr:np.ndarray, maille_vtheta:np.ndarray)->'tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray]': 
    """
    Converti les positions et vitesses d'un maillage en coordonées polaires à un maillage en coordonées cartésiennes 

    Entrées: 
    maille_r: ndarray bidimensionnel des positions radiales 
    maille_theta: ndarray bidimensionnel des positions angulaires 
    maille_vr: ndarray bidimensionnel des vitesses radiales 
    maille_vtheta: ndarray bidimensionnel des vitesses angulaires   

    Sorties:
    Tuple contenant, 
    maille_x: ndarray bidimensionnel des positions en horizontales en x  
    maille_y: ndarray bidimensionnel des positions verticales en y 
    maille_vx: ndarray bidimensionnel des vitesses en x  
    maille_vy: ndarray bidimensionnel des vitesses en y        
    """
    maille_x = maille_r*np.cos(maille_theta) 
    maille_y = maille_r*np.sin(maille_theta) 
    maille_vx = maille_vr*np.cos(maille_theta) - maille_vtheta*np.sin(maille_theta)
    maille_vy = maille_vr*np.sin(maille_theta) + maille_vtheta*np.cos(maille_theta)
    return maille_x, maille_y, maille_vx, maille_vy

def integrale(x:'list|np.ndarray', y:'list|np.ndarray')->float: 
    """ 
    Calcule une integrale avec la méthode des trapèzes pour des séries de valeurs discrètes
    
    Entrées: 
    x: Valeurs des abcisses 
    y: Valeurs des ordonnées 
    
    Sorties: 
    Résultat de l'intégrale sur toutes les valeurs 
    """ 
    N = len(x)-1 
    return 0.5*sum((x[i]-x[i-1])*(y[i]+y[i-1]) for i in range(1, N))

def cp(mesh_vr:np.ndarray, mesh_vtheta:np.ndarray, params:object)->np.ndarray: 
    """ 
    Évalue le coefficient de portance au bord du cylindre sur tout le domaine angulaire. 

    Entrées: 
    mesh_vr: Maille bidimensionnelle des vitesses radiales  
    mesh_theta: Maille bidimensionnelle des vitesses angulaires
    params: Objet contenant les paramètres du problème

    Sorties: 
    ndarray de taille (1 par nombre de noeuds en theta)  
    """
    # prennons les vitesses sur le bord gauche en polaire(0 à 2pi sur R)
    vr_bord = mesh_vr[:,0] 
    vtheta_bord = mesh_vtheta[:,0]
    vitesse = np.sqrt(vr_bord**2 + vtheta_bord**2) # norme de la vitesse 
    
    return 1 - np.sqrt(vitesse/params.u_inf)

def cd(cp:np.ndarray)->float: 
    """ 
    Évalue le coefficient de trainée au bord du cylindre sur tout le domaine angulaire. 

    Entrées: 
    cp: ndarray de taille (1 par nombre de noeuds en theta) des valeurs du coefficient de portance au bord du cylindre

    Sorties: 
    Valeur du coefficient de trainée 
    """
    ntheta = len(cp)
    domain = np.linspace(0, 2*np.pi, ntheta)
    integrande = cp*np.cos(domain) # fonction qu'on intègre pour avoir le cd 
    return -0.5*integrale(domain, integrande) 

def cl(cp:np.ndarray)->float: 
    """ 
    Évalue le coefficient de portance au bord du cylindre sur tout le domaine angulaire. 

    Entrées: 
    cp: ndarray de taille (1 par nombre de noeuds en theta) des valeurs du coefficient de portance au bord du cylindre

    Sorties: 
    Valeur du coefficient de portance 
    """
    ntheta = len(cp)
    domain = np.linspace(0, 2*np.pi, ntheta)
    integrande = cp*np.sin(domain) # fonction qu'on intègre pour avoir le cl 
    return -0.5*integrale(domain, integrande) 

def compute_coefficients(mesh_vr:np.ndarray, mesh_vtheta:np.ndarray, params:object)->None: 
    """ 
    Évalue les coefficients de pression, trainée et portance au bord du cylindre sur tout le domaine angulaire. 

    Entrées: 
    mesh_vr: Maille bidimensionnelle des vitesses radiales  
    mesh_theta: Maille bidimensionnelle des vitesses angulaires
    params: Objet contenant les paramètres du problème

    Sorties: 
    Aucune, la procédure imprime les résultats sur le terminal. 
    """
    cp_ = cp(mesh_vr, mesh_vtheta, params)
    cd_ = cd(cp_)
    cl_ = cl(cp_)
    print(f"--------------------\nCoefficients à r={params.R}m sur theta=[0,2pi]:")
    print(f"Coefficient de portance = {cp_}")
    print(f"Coefficient de trainée = {cd_}")
    print(f"Coefficient de portance = {cl_}", "--------------------", sep="\n")

if __name__ == "__main__": 
    """ 
    permet de lancer le fichier fonctions.py directement pour faire les tests 
    """
    pytest.main(['tests.py']) 