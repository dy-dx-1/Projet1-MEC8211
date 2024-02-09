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
profil_S_constant = solve.solveur_stationnaire(params, consommation_constante=True, ordre_derive_premiere=1)
profil_S_ordre1 = solve.solveur_stationnaire(params, consommation_constante=False, ordre_derive_premiere=1)

graphique("Profil de concentration selon le type de source", "Position radiale [m]", r"Concentration [mol/$m^3$]",
          (dom, profil_S_constant, r"$S=8*10^{-9}$", ".-"),
          (dom, profil_S_ordre1, r"$S=k*C$", ".-"))

### Question E: Comparaison entre sol stationnaire S constant et analytique 
# Le profil S constant a déjà été calculé
C_exact_domaine = C_exact(dom) # Concentration exacte évaluée sur le domaine de discrétisation 
graphique("Profil obtenu numériquement et analytiquement pour une source constante et approx dérivée première ordre 1", "Position radiale [m]", r"Concentration [mol/$m^3$]",
          (dom, profil_S_constant, f"Numérique avec {params.N=}", ".-"),
          (dom, C_exact_domaine, rf"Analytique avec {params.N=}", ".-"),
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

"""
data_instance = Data() 
tab_erreur=[[],[],[]]
tab_dr=[]

for n in range(1, 3):
    data_instance.Ntt = 5 * n
    tab_dr.append(data_instance.dr)

    if data_instance.stationnaire:
        Results = solver_stationnaire(data_instance)
        tableau_ana = analytique_sur_domaine(
            data_instance, [i * data_instance.dr for i in range(data_instance.Ntt)]
        )
    else:
        Results = solver(data_instance)
        tableau_ana = analytique_sur_domaine(
            data_instance, [i * data_instance.dr for i in range(data_instance.Ntt)]
        )
    graphique(data_instance, Results)

    tab_erreur[0].append(erreur_L1(data_instance, Results, tableau_ana))
    tab_erreur[1].append(erreur_L2(data_instance, Results, tableau_ana))
    tab_erreur[2].append(erreur_Linf(data_instance, Results, tableau_ana))

graphique_erreur(data_instance, tab_dr, tab_erreur)
""" 