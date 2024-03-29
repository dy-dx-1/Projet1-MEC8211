import numpy as np 
import solveurs as solve 
import erreurs as err
import visualisation as vis
import sympy as sp
import math as math

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

### Définition du problème 
class Data:  
    ro = 0.5  # Diamètre du cylindre [m]
    D = 10**(-10) # coeff diffusion effective 
    k = 4*(10**(-9)) # constante de réaction si réaction du premier ordre 
    C_ext = 12 # Concentration à l'extérieur 
    S = lambda r,t: 0 # Terme source permettant de vérifier la solution avec la MMS 

    N = 5
    domaine = np.linspace(0, ro, N)

    nb_annees = 100 # Durée de la simulation transitoire en années 
    t_sim = int(nb_annees*365.25*24*60*60) # temps de simulation en secondes

def Devoir1(): 
    params = Data() 
    n_values=[5,500]
    ### Solution analytique 
    # Définissons une fonction lambda pour évaluer facilement la solution analytique 
    C_exact = lambda r: np.true_divide(params.S,4*params.D)*np.square(params.ro)*(np.square(np.divide(r, params.ro))-1)+params.C_ext 
    dom_analytique = np.linspace(0, params.ro, 100) 
    C_exact_domaine = C_exact(dom_analytique) # Concentration exacte évaluée sur le domaine de discrétisation 

    ### Question D: Profil de concentration stationnaire avec S constant et coeff concentration ordre 1 ; le tout avec derivée premiere ordre 1
    profil_S_constant_trans = solve.solveur_transitoire(params, consommation_constante=True, ordre_derive_premiere=1)
    profil_S_ordre1_trans = solve.solveur_transitoire(params, consommation_constante=False, ordre_derive_premiere=1)
    graphiques_D = [(params.domaine, profil_S_constant_trans, r"$S=8*10^{-9}$", ".-"), (params.domaine, profil_S_ordre1_trans, r"$S=k*C$", ".-")]
    vis.show_graphs(f"Profil de concentration transitoire après 10 ans selon le type de source", "Position radiale [m]", r"Concentration [mol/$m^3$]", graphiques_D)
    ### Question E: Comparaison entre sol stationnaire S constant et analytique, avec derive_premiere d'ordre 1
    cas_a_resoudre = lambda: solve.solveur_stationnaire(params, consommation_constante=True, ordre_derive_premiere=1)
    graphiques_E = vis.generate_n_graphs(params, cas_a_resoudre, n_values)
    graphiques_E.append((dom_analytique, C_exact_domaine, "Analytique avec N = 100", "-")) 
    vis.show_graphs("Profil obtenu numériquement et analytiquement pour une source constante et approx dérivée première ordre 1", "Position radiale [m]", r"Concentration [mol/$m^3$]",
             graphiques_E)
    ### Question E)b): Sur un même graphique les erreurs L1, L2 et L∞. 
    Erreur_L1=[]
    Erreur_L2=[]
    Erreur_Linf=[]
    for i in range(len(n_values)):
        Erreur_L1.append(err.erreur_L1(graphiques_E[i][0],graphiques_E[i][1],C_exact(graphiques_E[i][0])))
        Erreur_L2.append(err.erreur_L2(graphiques_E[i][0],graphiques_E[i][1],C_exact(graphiques_E[i][0])))
        Erreur_Linf.append(err.erreur_Linf(graphiques_E[i][0],graphiques_E[i][1],C_exact(graphiques_E[i][0])))
       
    vis.graphique_erreur("ordre 1",n_values,[Erreur_L1,Erreur_L2,Erreur_Linf])
    err.erreur_de_convergence_observe(params,n_values,Erreur_L1,Erreur_L2,Erreur_Linf)
    # Valeurs exactes ne changent évidamment pas 
    cas_a_resoudre = lambda: solve.solveur_stationnaire(params, consommation_constante=True, ordre_derive_premiere=2)
    graphiques_D = vis.generate_n_graphs(params, cas_a_resoudre, n_values)
    graphiques_D.append((dom_analytique, C_exact_domaine, "Analytique avec N = 100", "-")) 
    vis.show_graphs("Profil obtenu numériquement et analytiquement pour une source constante et approx dérivée première ordre 2", "Position radiale [m]", r"Concentration [mol/$m^3$]",
             graphiques_D)
    # Question F)a)
    Erreur_L1=[]
    Erreur_L2=[]
    Erreur_Linf=[]
    for i in range(len(n_values)):
        Erreur_L1.append(err.erreur_L1(graphiques_D[i][0],graphiques_D[i][1],C_exact(graphiques_D[i][0])))
        Erreur_L2.append(err.erreur_L2(graphiques_D[i][0],graphiques_D[i][1],C_exact(graphiques_D[i][0])))
        Erreur_Linf.append(err.erreur_Linf(graphiques_D[i][0],graphiques_D[i][1],C_exact(graphiques_D[i][0])))
      
    #vis.graphique_erreur("ordre 2",n_values,[Erreur_L1,Erreur_L2,Erreur_Linf]) 
    #err.erreur_de_convergence_observe(params,n_values,Erreur_L1,Erreur_L2,Erreur_Linf)
    return None 

def Analyse_MMS_spatiale(params, C_exact_MMS_eval, t_sim): 
    """
    Analyse de convergence sur le domaine spatial avec la MMS. 
    params: Objet contenant les données de la simulation 
    C_exact_MMS_eval: Lambda retournant la valeur exacte de concentration pour la MMS  
    t_sim: temps total de simulation transitoire 
    """
    ## Préparation MMS
    dom_analytique = np.linspace(0, params.ro, 100)
    C_exact_domaine_MMS = C_exact_MMS_eval(dom_analytique, t_sim)
    ## Visualisation du profil de concentration avec différents noeuds
    n_vals = [4, 5, 10, 20, 25, 30, 40]
    drs=[params.ro/(n-1) for n in n_vals] # valeurs de dr correspondant aux différents noeuds 
    dt_impose = 1e4 # pas de temps fin pour tous les tests, à réduire si on veut plus de précision en échange d'augmenter le temps de calcul 
    # Simulations numériques MMS, n variable
    graphiques_multi_n = vis.generate_n_graphs(params, lambda: solve.solveur_transitoire(params, ordre_derive_premiere=2, dt=dt_impose), n_values=n_vals)
    # Solution exacte MMS 
    graphiques_multi_n.append((dom_analytique, C_exact_domaine_MMS, "Analytique avec N = 100", "-")) 
    # Plotting sol num et exacte 
    vis.show_graphs("Profil obtenu numériquement et analytiquement avec la MMS en variant le nb de noeuds", "Position radiale [m]", r"Concentration [mol/$m^3$]",
                graphiques_multi_n)
    # Calcul des erreurs 
    Erreurs_L1 = [err.erreur_L1(graphiques_multi_n[i][0],graphiques_multi_n[i][1],C_exact_MMS_eval(graphiques_multi_n[i][0], t_sim)) for i in range(len(n_vals))] 
    Erreurs_L2 = [err.erreur_L2(graphiques_multi_n[i][0],graphiques_multi_n[i][1],C_exact_MMS_eval(graphiques_multi_n[i][0], t_sim)) for i in range(len(n_vals))] 
    Erreurs_Linf = [err.erreur_Linf(graphiques_multi_n[i][0],graphiques_multi_n[i][1],C_exact_MMS_eval(graphiques_multi_n[i][0], t_sim)) for i in range(len(n_vals))] 
    ## Calcul de l'ordre de convergence et affichage 
    vis.graphique_convergence_erreurs(drs, [Erreurs_L1, Erreurs_L2, Erreurs_Linf], 'dr') 
    return 

def Analyse_MMS_temporelle(params, C_exact_MMS_eval, t_sim): 
    """
    Analyse de convergence sur le domaine temporel avec la MMS. 
    params: Objet contenant les données de la simulation 
    C_exact_MMS_eval: Lambda retournant la valeur exacte de concentration pour la MMS  
    t_sim: temps total de simulation transitoire 
    """
    ## Params généraux pour les simulations en temps
    params.N = 30 
    params.domaine = np.linspace(0, params.ro, params.N)
    dts = [1e9, 1e7, 2e6, 1e6, 5e5]
    ## Préparation MMS 
    dom_analytique = np.linspace(0, params.ro, params.N)
    C_exact_domaine_MMS = C_exact_MMS_eval(dom_analytique, t_sim)
    # Simulations numériques de la MMS en changeant le pas de temps 
    graphiques_multi_dt = vis.generate_dt_graphs(params, lambda dt_: solve.solveur_transitoire(params, ordre_derive_premiere=2, dt = dt_), dt_values=dts)
    # Solution exacte MMS
    graphiques_multi_dt.append((dom_analytique, C_exact_domaine_MMS, f"Analytique avec N = {params.N}", "-")) 
    ## Visualisation résultats MMS selon le pas de temps 
    vis.show_graphs(f"Profil obtenu numériquement et analytiquement avec la MMS en variant le pas de temps avec N={params.N}", "Position radiale [m]", r"Concentration [mol/$m^3$]",
                graphiques_multi_dt)
    # Calcul des erreurs 
    Erreurs_L1 = [err.erreur_L1(graphiques_multi_dt[i][0],graphiques_multi_dt[i][1],C_exact_MMS_eval(graphiques_multi_dt[i][0], t_sim)) for i in range(len(dts))] 
    Erreurs_L2 = [err.erreur_L2(graphiques_multi_dt[i][0],graphiques_multi_dt[i][1],C_exact_MMS_eval(graphiques_multi_dt[i][0], t_sim)) for i in range(len(dts))] 
    Erreurs_Linf = [err.erreur_Linf(graphiques_multi_dt[i][0],graphiques_multi_dt[i][1],C_exact_MMS_eval(graphiques_multi_dt[i][0], t_sim)) for i in range(len(dts))] 
    ## Calcul de l'ordre de convergence et affichage 
    vis.graphique_convergence_erreurs(dts, [Erreurs_L1, Erreurs_L2, Erreurs_Linf], 'dt')
    return

def Devoir2():
    ### Paramètres de la simulation
    params = Data() 
    t_sim = params.t_sim
    C_ext = params.C_ext
    R = params.ro
    D = params.D
    k = params.k
    
    ### Setup de la solution manufacturée 
    r = sp.symbols("r") 
    t = sp.symbols("t") 
    C_MMS = C_ext - sp.exp(-t/ t_sim) *((1 - ((r/R)**2)) * sp.sin(r+(np.pi/2))) 
    dC_MMS_r = sp.diff(C_MMS, r) 
    ddC_MMS_r = sp.diff(dC_MMS_r, r)
    dC_MMS_t = sp.diff(C_MMS, t)
    # Nouveau terme source pour accomoder C_MMS   
    params.S = sp.lambdify([r, t], dC_MMS_t - ((D/r)*dC_MMS_r) - (D*ddC_MMS_r) + (k*C_MMS), 'numpy')
    C_exact_MMS_eval = sp.lambdify([r,t], C_MMS, 'numpy') # permet d'evaluer la solution exacte de la MMS 
    ### Graphiques d'erreur 
    ##  Rafinement spatial, t fixe à t_sim
    Analyse_MMS_spatiale(params, C_exact_MMS_eval, t_sim) 
    ## Rafinement temporel, t fixe à t_sim et n fixe à 15 noeuds 
    Analyse_MMS_temporelle(params, C_exact_MMS_eval, t_sim) 
    return 

def main(): 
    Devoir2() 
    return 

if __name__=="__main__": 
    main()