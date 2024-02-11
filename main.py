# -*- coding: utf-8 -*-
"""
@authors: alcaru
"""
import numpy as np 
import solveurs as solve 
from erreurs import erreur_L1, erreur_L2, erreur_Linf
from visualisation import graphique, graphique_erreur

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
dom = params.domaine 

### Solution analytique 
# Définissons une fonction lambda pour évaluer facilement la solution analytique 
C_exact = lambda r: np.true_divide(params.S,4*params.D)*np.square(params.ro)*(np.square(np.divide(r, params.ro))-1)+params.C_ext 

### Question D: Profil de concentration stationnaire avec S constant et coeff concentration ordre 1 ; le tout avec derivée premiere ordre 1
profil_S_constant = solve.solveur_transitoire(params, consommation_constante=True, ordre_derive_premiere=1)
profil_S_ordre1 = solve.solveur_transitoire(params, consommation_constante=False, ordre_derive_premiere=1)

graphique("Profil de concentration selon le type de source", "Position radiale [m]", r"Concentration [mol/$m^3$]",
          (dom, profil_S_constant, r"$S=8*10^{-9}$", ".-"),
          (dom, profil_S_ordre1, r"$S=k*C$", ".-"))

### Question E: Comparaison entre sol stationnaire S constant et analytique 
# Le profil S constant a déjà été calculé
C_exact_domaine = C_exact(dom) # Concentration exacte évaluée sur le domaine de discrétisation 
graphique("Profil obtenu numériquement et analytiquement pour une source constante et approx dérivée première ordre 1", "Position radiale [m]", r"Concentration [mol/$m^3$]",
          (dom, profil_S_constant, f"Numérique avec {params.N=}", ".-"),
          (dom, C_exact_domaine,   f"Analytique avec {params.N=}", ".-"),
          (np.linspace(0, params.ro), C_exact(np.linspace(0, params.ro)), rf"Analytique avec N=50", "-"))
################################# TODO : Erreurs 

### Question F: Profils avec différentiation ordre 2 
# Valeurs exactes ne changent évidamment pas 
profil_S_cnst_ordre2 = solve.solveur_stationnaire(params, consommation_constante=True, ordre_derive_premiere=2)
graphique("Profil obtenu numériquement et analytiquement pour une source constante et approx dérivée première ordre 2", "Position radiale [m]", r"Concentration [mol/$m^3$]",
          (dom, profil_S_constant, f"Numérique avec {params.N=}", ".-"),
          (dom, C_exact_domaine, rf"Analytique avec {params.N=}", ".-"),
          (np.linspace(0, params.ro), C_exact(np.linspace(0, params.ro)), rf"Analytique avec N=50", "-"))
################################# TODO : Erreurs 
