import fonctions as f 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.interpolate import interp1d

from graphique_convergence import  graphique_convergence_erreurs,erreur_L1,erreur_L2,erreur_Linf

class Parametres():
    u_inf = 1 
    R = 1 
    R_ext = 5 
    
    theta_min = 0 
    theta_max = 2 * np.pi 

    nx = 15
    ny = 30

def prediction():
    
    def calculate_GCI(p_g, frh, fh):
        """
        Fonction calculant le Grid Convergence Index (GCI) pour notre cas précis
    
        Parameters
        ----------
        p_g : float
            Paramètre p utilisé dans le calcul de GCI.
        frh : float
            Fréquence relative haute.
        fh : float
            Fréquence haute.
    
        Returns
        -------
        gci : float
        Grid Convergence Index (GCI)
        """
        p = min(max(0.5, p_g), 4)  # Assure que p est dans l'intervalle [0.5, 4.0]
        return (3 / (2**p - 1)) * abs(frh - fh)
    
    def f_err(tab1,tab2):
        """
        Fonction calculant l'erreur L1 entre deux tableaux.
    
        Parameters
        ----------
        tab1 : array_like
            Resultat analytique ou numérique
        tab2 : array_like
            Resultas analytique ou numérique
        Returns
        -------
        res : list
            Liste contenant les valeurs absolues des différences entre les éléments correspondants des deux tableaux.
    
        Raises
        ------
        ValueError
            Si les deux tableaux n'ont pas la même longueur.
        """
        res=[]
        for i in range(len(tab1)):
               res.append((abs((tab1[i]-tab2[i]))))
        return res 

    prm = Parametres()
    
    errL1=[]
    errL2=[]
    errLinf=[]
    nb_noeuds=30
    nb_fin_noeuds=85
    u_infs=[0.1*i for i in range(5,35,5)]
    
    Resultats_Cd,Resultats_Cl=[],[]
    Resultats_fin_Cd,Resultats_fin_Cl=[],[]
    
    GCI_cd,GCI_cl=[],[]
    
    for u_inf in u_infs: 
        prm.u_inf=u_inf
        print("Calculating for u_inf = ", u_inf)
        prm.nx = nb_noeuds
        prm.ny = nb_noeuds

        # on recalcule les caractéristiques de la situation avec la mdf 
        r_mesh, theta_mesh, vecteur_psis = f.mdf(params=prm)
        psi_mdf_mesh = f.arrange_mesh(vecteur_psis, prm.nx, prm.ny) # valeurs de psi calculées par mdf sur maillage 
        vr, vtheta = f.vitesses(vecteur_psis, prm) 
        vr_mesh, vtheta_mesh = f.arrange_mesh(vr, prm.nx, prm.ny), f.arrange_mesh(vtheta, prm.nx, prm.ny) 
        
        # Output des coefficients de pression, portance et trainée 
        cp,cd,cl=f.compute_coefficients(vr_mesh, vtheta_mesh, prm)
        Resultats_Cd.append(cd)
        Resultats_Cl.append(cl)
        
        
        
        
        fiter_noeud=[43,46,49]

        cd_ana,cl_ana,cd_mesh,cl_mesh=[],[],[],[]
        for noeud_intermed in fiter_noeud:
            prm.nx = noeud_intermed
            prm.ny = noeud_intermed
            # on recalcule les caractéristiques de la situation avec la mdf 
            r_mesh, theta_mesh, vecteur_psis = f.mdf(params=prm)
            psi_mdf_mesh = f.arrange_mesh(vecteur_psis, prm.nx, prm.ny) # valeurs de psi calculées par mdf sur maillage 
            vr, vtheta = f.vitesses(vecteur_psis, prm) 
            vr_mesh, vtheta_mesh = f.arrange_mesh(vr, prm.nx, prm.ny), f.arrange_mesh(vtheta, prm.nx, prm.ny) 
            vr_mesh_ref, vtheta_mesh_ref = f.vr_ref_mesh(prm), f.vtheta_ref_mesh(prm) # valeurs de vitesse analytique sur maillage 

            
            cp,Cd_mesh,Cl_mesh=f.compute_coefficients(vr_mesh, vtheta_mesh, prm)
            cp,Cd_ana,Cl_ana=f.compute_coefficients(vr_mesh_ref, vtheta_mesh_ref, prm)
            
            cd_ana.append(Cd_ana)
            cl_ana.append(Cl_ana)
            cd_mesh.append(Cd_mesh)
            cl_mesh.append(Cl_mesh)
            
            
        errCD=f_err(cd_ana,cd_mesh)
        errCL=f_err(cl_ana,cl_mesh)

        coeffCd = np.polyfit(np.log(fiter_noeud), np.log(errCD), 1)
        ordreCd = coeffCd[0] 
        print("ordreCd",ordreCd)
        coeffCl = np.polyfit(np.log(fiter_noeud), np.log(errCL), 1)
        ordreCl = coeffCl[0]
        print("ordreCl",ordreCl)
        
        ###Calcul maillage fin
        
        prm.nx = nb_fin_noeuds
        prm.ny = nb_fin_noeuds

        # on recalcule les caractéristiques de la situation avec la mdf 
        r_mesh, theta_mesh, vecteur_psis = f.mdf(params=prm)
        psi_mdf_mesh = f.arrange_mesh(vecteur_psis, prm.nx, prm.ny) # valeurs de psi calculées par mdf sur maillage 
        vr, vtheta = f.vitesses(vecteur_psis, prm) 
        vr_mesh, vtheta_mesh = f.arrange_mesh(vr, prm.nx, prm.ny), f.arrange_mesh(vtheta, prm.nx, prm.ny) 
        
        # Output des coefficients de pression, portance et trainée 
        cp,cd,cl=f.compute_coefficients(vr_mesh, vtheta_mesh, prm)
        Resultats_fin_Cd.append(cd)
        Resultats_fin_Cl.append(cl)
        
        GCI_cd.append(calculate_GCI(ordreCd, cd, cd_mesh[0]))
        GCI_cl.append(calculate_GCI(ordreCl, cl, cl_mesh[0]))
        print("GCI_cd",GCI_cd)
        print("GCI_cl",GCI_cl)   
    
    E_Cd = [abs(Resultats_fin_Cd[0]-Resultats_Cd[i]) for i in range(len(u_infs))]
    E_Cl = [abs(Resultats_fin_Cl[0]-Resultats_Cl[i]) for i in range(len(u_infs))]
    
    print("E_Cd",E_Cd)
    print("E_Cl",E_Cl)

    # Définition des valeurs et de leurs incertitudes pour chaque cas
    
    #Unum1=5.2e-5
    #Unum2=1.3e-4
    

    incertitudes_Cd = [2*GCI_cd[i] for i in range(len(u_infs))]
    incertitudes_Cl = [2*GCI_cl[i] for i in range(len(u_infs))]
    
    print("incertitudes_Cd",incertitudes_Cd)
    print("incertitudes_Cl",incertitudes_Cl)
    
    couleurs_Cd = ['blue' for i in range(len(u_infs))]
    couleurs_Cl = ['red' for i in range(len(u_infs))]
    
    #Prediction Cd
    x = [i for i in range(len(u_infs))]
    y_up = [E_Cd[i] + incertitudes_Cd[i] / 2 for i in range(len(E_Cd))]
    y_mid = E_Cd
    y_down = [E_Cd[i] - incertitudes_Cd[i] / 2 for i in range(len(E_Cd))]
    
    coeff_up = np.polyfit(x, y_up, 1)
    coeff_mid = np.polyfit(x, y_mid, 1)
    coeff_down = np.polyfit(x, y_down, 1)
    
    f_up = np.poly1d(coeff_up)
    f_mid = np.poly1d(coeff_mid)
    f_down = np.poly1d(coeff_down)
    
    predi_CD = [f_mid(100), f_up(100) - f_down(100)]

    #Prediction Cl
    y_up = [E_Cl[i] + incertitudes_Cl[i] / 2 for i in range(len(E_Cl))]
    y_mid = E_Cl
    y_down = [E_Cl[i] - incertitudes_Cl[i] / 2 for i in range(len(E_Cl))]
    
    coeff_up = np.polyfit(x, y_up, 1)
    coeff_mid = np.polyfit(x, y_mid, 1)
    coeff_down = np.polyfit(x, y_down, 1)
    
    f_up = np.poly1d(coeff_up)
    f_mid = np.poly1d(coeff_mid)
    f_down = np.poly1d(coeff_down)

    predi_Cl = [f_mid(100), f_up(100) - f_down(100)]

    
    
    
    plt.figure(1)
    # Création du graphique pour chaque cas
    for i in range(len(u_infs)):
        plt.errorbar(i + 1, E_Cd[i], yerr=incertitudes_Cd[i], fmt='o', capsize=5, color=couleurs_Cd[i], markersize=8)
    
    # Ajout des valeurs extrapolées en violet
    plt.plot(len(u_infs) + 1, predi_CD[0], marker='o', color='purple', markersize=8, label='Extrapolated Value')
    plt.errorbar(len(u_infs) + 1, predi_CD[0], yerr=predi_CD[1], fmt='_', color='purple', markersize=8)
    
    # Ajout des étiquettes pour chaque cas au niveau de l'axe des abscisses
    plt.xticks([i for i in range(len(u_infs)+2)], ["0"]+[str(u_infs[i]) for i in range(len(u_infs))]+["100"])
    
    # Ajout du titre et des labels d'axes
    plt.title('Graphique avec incertitudes')
    plt.xlabel('Situations')
    plt.ylabel('Δ(deltamodele)')
    plt.legend()
    plt.savefig('graphique_Cd_prédiction.png')
    # Affichage du graphique
    plt.show()
    
    plt.figure(2)
    # Création du graphique pour chaque cas
    for i in range(len(u_infs)):
        plt.errorbar(i + 1, E_Cl[i], yerr=incertitudes_Cl[i], fmt='o', capsize=5, color=couleurs_Cl[i], markersize=8)
    
    # Ajout des valeurs extrapolées en violet
    plt.plot(len(u_infs) + 1, predi_Cl[0], marker='o', color='purple', markersize=8, label='Extrapolated Value')
    plt.errorbar(len(u_infs) + 1, predi_Cl[0], yerr=predi_Cl[1], fmt='_', color='purple', markersize=8)
    
    # Ajout des étiquettes pour chaque cas au niveau de l'axe des abscisses
    plt.xticks([i for i in range(len(u_infs))], ["0"]+[str(u_infs[i]) for i in range(len(u_infs))]+["100"])
    
    # Ajout du titre et des labels d'axes
    plt.title('Graphique avec incertitudes')
    plt.xlabel('U_infs')
    plt.ylabel('Δ(deltamodele)')
    plt.legend()
    plt.savefig('graphique_Cl_prédiction.png')
    # Affichage du graphique
    plt.show()

if __name__=="__main__": 
    prediction()
    