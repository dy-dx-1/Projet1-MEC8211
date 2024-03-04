# -*- coding: utf-8 -*-
import numpy as np 
import solveurs as solve 
from erreurs import erreur_L1, erreur_L2, erreur_Linf,erreur_de_convergence_observe
from visualisation import show_graphs, graphique_erreur, generate_n_graphs
import matplotlib.pyplot as plt
import sympy as sp
import math as math

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
    show_graphs(f"Profil de concentration transitoire après 10 ans selon le type de source", "Position radiale [m]", r"Concentration [mol/$m^3$]", graphiques_D)
    ### Question E: Comparaison entre sol stationnaire S constant et analytique, avec derive_premiere d'ordre 1
    cas_a_resoudre = lambda: solve.solveur_stationnaire(params, consommation_constante=True, ordre_derive_premiere=1)
    graphiques_E = generate_n_graphs(params, cas_a_resoudre, n_values)
    graphiques_E.append((dom_analytique, C_exact_domaine, "Analytique avec N = 100", "-")) 
    show_graphs("Profil obtenu numériquement et analytiquement pour une source constante et approx dérivée première ordre 1", "Position radiale [m]", r"Concentration [mol/$m^3$]",
             graphiques_E)
    ### Question E)b): Sur un même graphique les erreurs L1, L2 et L∞. 
    Erreur_L1=[]
    Erreur_L2=[]
    Erreur_Linf=[]
    for i in range(len(n_values)):
        Erreur_L1.append(erreur_L1(graphiques_E[i][0],graphiques_E[i][1],C_exact(graphiques_E[i][0])))
        Erreur_L2.append(erreur_L2(graphiques_E[i][0],graphiques_E[i][1],C_exact(graphiques_E[i][0])))
        Erreur_Linf.append(erreur_Linf(graphiques_E[i][0],graphiques_E[i][1],C_exact(graphiques_E[i][0])))
       
    graphique_erreur("ordre 1",n_values,[Erreur_L1,Erreur_L2,Erreur_Linf])
    erreur_de_convergence_observe(params,n_values,Erreur_L1,Erreur_L2,Erreur_Linf)
    # Valeurs exactes ne changent évidamment pas 
    cas_a_resoudre = lambda: solve.solveur_stationnaire(params, consommation_constante=True, ordre_derive_premiere=2)
    graphiques_D = generate_n_graphs(params, cas_a_resoudre, n_values)
    graphiques_D.append((dom_analytique, C_exact_domaine, "Analytique avec N = 100", "-")) 
    show_graphs("Profil obtenu numériquement et analytiquement pour une source constante et approx dérivée première ordre 2", "Position radiale [m]", r"Concentration [mol/$m^3$]",
             graphiques_D)
    # Question F)a)
    Erreur_L1=[]
    Erreur_L2=[]
    Erreur_Linf=[]
    for i in range(len(n_values)):
         Erreur_L1.append(erreur_L1(graphiques_D[i][0],graphiques_D[i][1],C_exact(graphiques_D[i][0])))
         Erreur_L2.append(erreur_L2(graphiques_D[i][0],graphiques_D[i][1],C_exact(graphiques_D[i][0])))
         Erreur_Linf.append(erreur_Linf(graphiques_D[i][0],graphiques_D[i][1],C_exact(graphiques_D[i][0])))
      
    #graphique_erreur("ordre 2",n_values,[Erreur_L1,Erreur_L2,Erreur_Linf]) 
    #erreur_de_convergence_observe(params,n_values,Erreur_L1,Erreur_L2,Erreur_Linf)
    return None 

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
    C_MMS = C_ext + (t * (1 - ((r/R)**2)) * sp.cos(r) / t_sim)
    dC_MMS_r = sp.diff(C_MMS, r) 
    ddC_MMS_r = sp.diff(dC_MMS_r, r)
    dC_MMS_t = sp.diff(C_MMS, t)
    # Nouveau terme source pour accomoder C_MMS   
    params.S = sp.lambdify([r, t], dC_MMS_t - ((D/r)*dC_MMS_r) - (D*ddC_MMS_r) + (k*C_MMS), 'numpy')
    
    ### Évaluation de la MMS et visualisation 
    dom_analytique = np.linspace(0, params.ro, 100)
    C_exact_domaine_MMS = sp.lambdify([r,t], C_MMS, 'numpy')(dom_analytique, t_sim)
    # Solution de la MMS avec notre solveur 
    Solution_MMS = solve.solveur_transitoire(params, ordre_derive_premiere=2)
    
    print(f"{Solution_MMS=}")
    plt.plot(dom_analytique,C_exact_domaine_MMS,label="Analytique")
    plt.plot(params.domaine,Solution_MMS,label="MMS")
    plt.legend()
    plt.show()
    return 

def main(): 
    Devoir2() 
    return 

if __name__=="__main__": 
    main() 