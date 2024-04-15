import fonctions as f 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.interpolate import interp1d

from  MMS.graphique_convergence import  graphique_convergence_erreurs,erreur_L1,erreur_L2,erreur_Linf

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
    noeuds_err = range(16,42, 2) # valeurs qu'on imposera aux noeuds 
    erreurs_psi, erreurs_vitesses = list(), list() 
    errL1,errL2,errLinf=[],[],[]
    errL1V,errL2V,errLinfV=[],[],[]
    
    cd_ana,cl_ana,cd_mesh,cl_mesh=[],[],[],[]
    
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
        
        cp,Cd_mesh,Cl_mesh=f.compute_coefficients(vr_mesh, vtheta_mesh, prm)
        cp,Cd_ana,Cl_ana=f.compute_coefficients(vr_mesh_ref, vtheta_mesh_ref, prm)
        
        cd_ana.append(Cd_ana)
        cl_ana.append(Cl_ana)
        cd_mesh.append(Cd_mesh)
        cl_mesh.append(Cl_mesh)
       
        # # On evalue l'erreur nouvelle methode
        domaine = [i for i in range(prm.nx)]
        errL1.append(erreur_L1(domaine, psi_mdf_mesh, psi_analytique_mesh))
        errL2.append(erreur_L2(domaine, psi_mdf_mesh, psi_analytique_mesh))
        errLinf.append(erreur_Linf(domaine, psi_mdf_mesh, psi_analytique_mesh))
        
        errL1V.append(erreur_L1(domaine, vitesses_mdf, vitesses_ref))
        errL2V.append(erreur_L2(domaine, vitesses_mdf, vitesses_ref))
        errLinfV.append(erreur_Linf(domaine, vitesses_mdf, vitesses_ref))
    
    #Graphiques de l'erreur
    erreurs=[errL1,errL2,errLinf]
    erreursV=[errL1V,errL2V,errLinfV]
    r_min, r_max, theta_min, theta_max = prm.R, prm.R_ext, prm.theta_min, prm .theta_max
    
    #dr = lambda nx: abs(r_max-r_min)/(nx-1)
    #dtheta = lambda ny: abs(theta_max-theta_min)/(ny-1)
    tab=[1/(i) for i in noeuds_err]
    #tab=np.array([dr(i)*dtheta(i) for i in noeuds_err])
    print(tab)
    #graphique_convergence_erreurs(tab,erreurs,'psi')
    #graphique_convergence_erreurs(tab,erreursV,'vitesse')
    
    def f_err(tab1,tab2):
        res=[]
        for i in range(len(tab1)):
            res.append((abs((tab1[i]-tab2[i]))))
        return res
        
    errCD=f_err(cd_ana,cd_mesh)
    errCL=f_err(cl_ana,cl_mesh)
    
    graphique_convergence_erreurs(tab,[errCD,errCD,errCD], "CD")
    graphique_convergence_erreurs(tab,[errCL,errCL,errCL], "CL")
    
    
def propagation():
    ### Résolution du problème avec paramètres initaux 
    prm = Parametres()
    
    errL1=[]
    errL2=[]
    errLinf=[]
    nb_noeuds=30
    u_infs=[2.061310662883705, 2.154424105908013, 2.2856514500180456, 2.067671558580253, 2.1901788697100777, 1.9590485907246835, 1.9321672769456182, 1.7451284369326179, 1.7368112458456166, 1.9248041055947231, 1.796247756076586, 1.7860735259840386, 2.0733857796113044, 2.0332534536591162, 2.070272113088028, 2.021006633312873, 2.683964340967518, 2.2805754357880104, 1.9325438791200482, 1.9646651719532797, 1.8302342690267055, 1.94410046354528, 1.862103124129983, 1.7424495742954367, 2.678843858912365]
    Resultats_Cd,Resultats_Cl=[],[]
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
       
    #PST tire de propagation des incertitude
    # traitement des résultats
    
    def printres(res,nom):
        # Calculer la moyenne et l'écart type
        moyenne = np.mean(res)
        ecart_type = np.std(res)
        median = np.median(res)
    
        print("Moyenne de "+nom+" :", moyenne)
        print("Écart type de "+nom+" :", ecart_type)
        print("Medianne de "+nom+" :", median)
    
        # Calculer la CDF de vos résultats de sortie
        sorted_srq = np.sort(res)
        cdf = np.arange(1, len(res) + 1) / len(res)
    
        # Tracer la CDF
        plt.plot(sorted_srq, cdf)
        plt.xlabel('Valeur de sortie')
        plt.ylabel('Probabilité cumulative')
        plt.title('CDF de la sortie SRQ='+nom)
        plt.grid(True)
        plt.savefig("CDF_de_la_sortie_"+nom+".png")
        plt.show()
    
    printres(Resultats_Cd,"Cd")
    printres(Resultats_Cl,"Cl")
   
def prediction():
    
    def calculate_GCI(p_g, frh, fh):
        p = min(max(0.5, p_g), 4)  # Assure que p est dans l'intervalle [0.5, 4.0]
        return (3 / (2**p - 1)) * abs(frh - fh)

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
        
        
        
        
        fiter_noeud=[43,45,50]

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
            
        def f_err(tab1,tab2):
                res=[]
                for i in range(len(tab1)):
                    res.append((abs((tab1[i]-tab2[i]))))
                return res     
        errCD=f_err(cd_ana,cd_mesh)
        errCL=f_err(cl_ana,cl_mesh)

        coeffCd = np.polyfit(np.log(fiter_noeud), np.log(errCD), 1)
        ordreCd = coeffCd[0] 
        coeffCl = np.polyfit(np.log(fiter_noeud), np.log(errCL), 1)
        ordreCl = coeffCd[0] 
        
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
        
        GCI_cd.append(calculate_GCI(ordreCd, cd, cd_mesh[1]))
        GCI_cl.append(calculate_GCI(ordreCl, cl, cl_mesh[1]))
            
    
    E_Cd = [abs(Resultats_fin_Cd-Resultats_Cd[i]) for i in range(len(u_infs))]
    E_Cl = [abs(Resultats_fin_Cl-Resultats_Cl[i]) for i in range(len(u_infs))]
    

    # Définition des valeurs et de leurs incertitudes pour chaque cas
    
    #Unum1=5.2e-5
    #Unum2=1.3e-4
    

    incertitudes_Cd = [2*GCI_cd[i] for i in range(len(u_infs))]
    incertitudes_Cl = [2*GCI_cl[i] for i in range(len(u_infs))]
    couleurs_Cd = ['blue' for i in range(len(u_infs))]
    couleurs_Cl = ['red' for i in range(len(u_infs))]
    
    plt.figure(1)
    # Création du graphique pour chaque cas
    for i in range(len(u_infs)):
        plt.errorbar(i + 1, E_Cd[i], yerr=incertitudes_Cd[i], fmt='o', capsize=5, color=couleurs_Cd[i], markersize=8)
    # Ajout d'une ligne en pointillés à zéro
    #plt.axhline(y=0, color='black', linestyle='--')

    # Ajout des étiquettes pour chaque cas au niveau de l'axe des abscisses
    plt.xticks([i for i in range(len(u_infs))], ["u_inf = "+str(u_infs[i]) for i in range(len(u_infs))])

    # Ajout du titre et des labels d'axes
    plt.title('Graphique avec incertitudes')
    plt.xlabel('Situations')
    plt.ylabel('Δ(deltamodele)')
    plt.savefig('graphique_Cd_prédiction.png')
    # Affichage du graphique
    plt.show()
    
    plt.figure(2)
    # Création du graphique pour chaque cas
    for i in range(len(u_infs)):
        plt.errorbar(i + 1, E_Cl[i], yerr=incertitudes_Cl[i], fmt='o', capsize=5, color=couleurs_Cl[i], markersize=8)
    # Ajout d'une ligne en pointillés à zéro
    #plt.axhline(y=0, color='black', linestyle='--')

    # Ajout des étiquettes pour chaque cas au niveau de l'axe des abscisses
    plt.xticks([i for i in range(len(u_infs))], ["u_inf = "+str(u_infs[i]) for i in range(len(u_infs))])

    # Ajout du titre et des labels d'axes
    plt.title('Graphique avec incertitudes')
    plt.xlabel('Situations')
    plt.ylabel('Δ(deltamodele)')
    plt.savefig('graphique_Cd_prédiction.png')
    # Affichage du graphique
    plt.show()
    
if __name__=="__main__": 
    #propagation()
    #main()
    prediction()
    