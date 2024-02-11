# -*- coding: utf-8 -*-
"""
@authors: alcaru
"""
import numpy as np 
import solveurs as solve 
from erreurs import erreur_L1, erreur_L2, erreur_Linf
from visualisation import show_graphs, graphique_erreur, generate_n_graphs

### Définition du problème 
class Data:  
    ro = 0.5  # Diamètre du cylindre [m]
    D = 10**(-10) # coeff diffusion effective 
    S = 8*(10**(-9)) # terme source si constant 
    k = 4*(10**(-9)) # constante de réaction si réaction du premier ordre 
    C_ext = 12 # Concentration à l'extérieur 

    N = 5 
    domaine = np.linspace(0, ro, N)
params = Data() 

### Solution analytique 
# Définissons une fonction lambda pour évaluer facilement la solution analytique 
C_exact = lambda r: np.true_divide(params.S,4*params.D)*np.square(params.ro)*(np.square(np.divide(r, params.ro))-1)+params.C_ext 
dom_analytique = np.linspace(0, params.ro, 100) 
C_exact_domaine = C_exact(dom_analytique) # Concentration exacte évaluée sur le domaine de discrétisation 

### Question D: Profil de concentration stationnaire avec S constant et coeff concentration ordre 1 ; le tout avec derivée premiere ordre 1
#profil_S_constant_trans = solve.solveur_transitoire(params, consommation_constante=True, ordre_derive_premiere=1)
#profil_S_ordre1_trans = solve.solveur_transitoire(params, consommation_constante=False, ordre_derive_premiere=1)
#graphiques_D = [(dom, profil_S_constant_trans, r"$S=8*10^{-9}$", ".-"), (dom, profil_S_ordre1_trans, r"$S=k*C$", ".-")]
#graphique(f"Profil de concentration transitoire après 10 ans selon le type de source", "Position radiale [m]", r"Concentration [mol/$m^3$]", graphiques_D)

### Question E: Comparaison entre sol stationnaire S constant et analytique, avec derive_premiere d'ordre 1
cas_a_resoudre = lambda: solve.solveur_stationnaire(params, consommation_constante=True, ordre_derive_premiere=1)
graphiques_E = generate_n_graphs(params, cas_a_resoudre, n_values=[5, 20, 50])
graphiques_E.append((dom_analytique, C_exact_domaine, f"Analytique avec N = 100", "-")) 
show_graphs("Profil obtenu numériquement et analytiquement pour une source constante et approx dérivée première ordre 1", "Position radiale [m]", r"Concentration [mol/$m^3$]",
          graphiques_E)
################################# TODO : Erreurs 

### Question F: Profils avec différentiation ordre 2 
# Valeurs exactes ne changent évidamment pas 
cas_a_resoudre = lambda: solve.solveur_stationnaire(params, consommation_constante=True, ordre_derive_premiere=2)
graphiques_D = generate_n_graphs(params, cas_a_resoudre, n_values=[5, 20, 50])
graphiques_D.append((dom_analytique, C_exact_domaine, f"Analytique avec N = 100", "-")) 
show_graphs("Profil obtenu numériquement et analytiquement pour une source constante et approx dérivée première ordre 2", "Position radiale [m]", r"Concentration [mol/$m^3$]",
          graphiques_D)
################################# TODO : Erreurs 
