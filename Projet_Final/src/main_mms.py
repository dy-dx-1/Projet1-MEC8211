
import numpy as np 
import matplotlib.pyplot as plt 

from  graphique_convergence import  graphique_convergence_erreurs,erreur_L1,erreur_L2,erreur_Linf
import fonctions_MMS as f 

class Parametres():
    u_inf = 1 
    R = 1 
    R_ext = 5 
    
    theta_min = 0 
    theta_max = 2 * np.pi 

    nx = 15
    ny = 30

def main():

    ### Résolution du problème avec paramètres initaux 
    prm = Parametres()

    ## Tout d'abord on résout le problème avec la mdf 
    r_mesh, theta_mesh, vecteur_psis = f.mdf(params=prm)

    # Obtention des vitesses sous forme de vecteur de noeuds 1d à l'aide des solutions de la mdf
    vr, vtheta = f.vitesses(vecteur_psis, prm) 

    # On fait passer les vitesses du vecteur correspondant aux k noeuds à des arrays 2d représentant la maille
    vr_mesh = f.arrange_mesh(vr, prm.nx, prm.ny) 
    vtheta_mesh = f.arrange_mesh(vtheta, prm.nx, prm.ny) 

    # On converti les arrays 2d des coordonnées et vitesses polaires sur la maille en leur équivalent cartésiens 
    x_mesh, y_mesh, vx_mesh, vy_mesh = f.convert_coords(r_mesh, theta_mesh, vr_mesh, vtheta_mesh) 

    # Output des coefficients de pression, portance et trainée 
    f.compute_coefficients(vr_mesh, vtheta_mesh, prm) 
    
    ## Graphique des vitesses sur le plan cartésien  
    fig, ax = plt.subplots() 
    ax.quiver(x_mesh, y_mesh, vx_mesh, vy_mesh)
    # ajout d'un cercle pour representer le cylindre et le domaine 
    cyl = plt.Circle((0,0), prm.R, color="r", fill=False, label="Cylindre")
    domaine = plt.Circle((0,0), prm.R_ext, color="b", fill=False, label="Domaine")
    ax.add_patch(cyl) 
    ax.add_patch(domaine)
    # Labels 
    ax.legend() 
    ax.set_xlabel("Coordonnées en x")
    ax.set_ylabel("Coordonnées en y")
    ax.set_title(f"Champ de vitesses du fluide autour d'un cylindre de rayon 1m avec nx=15 et ny=30 noeuds")
    # Cleanup de l'affichage 
    ax.set_aspect('equal', 'box')
    ax.grid(True) 
    plt.show() 

    ### Analyse de l'effet des erreurs 
    # On fera un graphique de l'erreur relative sur les psis et sur la norme de la vitesse pour différents nombre de noeuds
    # pour faciliter l'analyse, on considèrera que nx = ny  
    noeuds_err = range(5,55, 5) # valeurs qu'on imposera aux noeuds 
    erreurs_psi, erreurs_vitesses = list(), list() 
    errL1,errL2,errLinf=[],[],[]
    errL1V,errL2V,errLinfV=[],[],[]
    
    for nb_noeuds in noeuds_err: 
        print("Calculating ", nb_noeuds)
        prm.nx = nb_noeuds
        prm.ny = nb_noeuds

        # on recalcule les caractéristiques de la situation avec la mdf 
        r_mesh, theta_mesh, vecteur_psis = f.mdf(params=prm)
        psi_mdf_mesh = f.arrange_mesh(vecteur_psis, prm.nx, prm.ny) # valeurs de psi calculées par mdf sur maillage 
        vr, vtheta = f.vitesses(vecteur_psis, prm) 
        vr_mesh, vtheta_mesh = f.arrange_mesh(vr, prm.nx, prm.ny), f.arrange_mesh(vtheta, prm.nx, prm.ny) 
        # on calcule les solutions analytiques associées 
        psi_analytique_mesh = f.psi_ref_mesh(prm) # valeurs de psi analytique sur le maillage 
        vr_mesh_ref, vtheta_mesh_ref = f.vr_ref_mesh(prm), f.vtheta_ref_mesh(prm) # valeurs de vitesse analytique sur maillage 

        # On utilise la norme de la vitesse pour calculer l'erreur associée, pour générer les erreurs, on n'a pas besoin de convertir en cartésien 
        vitesses_ref = np.sqrt(vr_mesh_ref**2 + vtheta_mesh_ref**2) # normes de la vitesse analytique 
        vitesses_mdf = np.sqrt(vr_mesh**2 + vtheta_mesh**2) # normes de la vitesse par mdf 
        
        # On evalue l'erreur 
        # erreur_relative_array = lambda arr_theo, arr_mdf: (np.average(abs(arr_theo-arr_mdf+1e-10)/(arr_theo+1e-10)))*100 # on perturbe de 1e-10 pour éviter /0
        # erreurs_psi.append(erreur_relative_array(psi_analytique_mesh, psi_mdf_mesh)) # erreur relative en %
        # erreurs_vitesses.append(erreur_relative_array(vitesses_ref, vitesses_mdf)) 
        # # On evalue l'erreur nouvelle methode
        domaine = [i for i in range(prm.nx)]
        errL1.append(erreur_L1(domaine, psi_mdf_mesh, psi_analytique_mesh))
        errL2.append(erreur_L2(domaine, psi_mdf_mesh, psi_analytique_mesh))
        errLinf.append(erreur_Linf(domaine, psi_mdf_mesh, psi_analytique_mesh))
        
        errL1V.append(erreur_L1(domaine, vitesses_mdf, vitesses_ref))
        errL2V.append(erreur_L2(domaine, vitesses_mdf, vitesses_ref))
        errLinfV.append(erreur_Linf(domaine, vitesses_mdf, vitesses_ref))
    
   # # Faisons le graphique 
   #  fig, axs = plt.subplots(2,1) 
   #  ax1, ax2 = axs[0], axs[1]
    
   #  ax1.plot(noeuds_err, erreurs_psi, '.-g', label="Erreur sur $\psi$") 
   #  ax2.plot(noeuds_err, erreurs_vitesses, '.-b', label="Erreur sur la vitesse") 

   #  ax1.set_title(r"Erreur relative sur $\psi$ et les vitesses selon la taille du maillage")
   #  ax1.set_ylabel(r"Erreur relative par rapport à la solution analytique[%]")
   #  ax1.grid(True) 
   #  ax1.legend() 

   #  ax2.set_xlabel(r"Nombre de noeuds sur le bord $nx=ny$")
   #  ax2.set_ylabel(r"Erreur relative par rapport à la solution analytique[%]")
   #  ax2.grid(True) 
   #  ax2.legend()    
   #  plt.show() 
    
    #Graphiques de l'erreur
    erreurs=[errL1,errL2,errLinf]
    erreursV=[errL1V,errL2V,errLinfV]
    r_min, r_max, theta_min, theta_max = prm.R, prm.R_ext, prm.theta_min, prm .theta_max
    
    #dr = lambda nx: abs(r_max-r_min)/(nx-1)
    #dtheta = lambda ny: abs(theta_max-theta_min)/(ny-1)
    tab=[10/i for i in range(5,55, 5)]
    #tab=np.array([dr(i)*dtheta(i) for i in noeuds_err])
    print(tab)
   
    graphique_convergence_erreurs(tab,erreurs,'psi')
    graphique_convergence_erreurs(tab,erreursV,'vitesse')
    
if __name__=="__main__": 
    main() 