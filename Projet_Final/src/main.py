import fonctions as f 
import numpy as np 
import matplotlib.pyplot as plt 

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
    noeuds_err = range(5, 55, 5) # valeurs qu'on imposera aux noeuds 
    erreurs_psi, erreurs_vitesses = list(), list() 
    errL1,errL2,errLinf=[],[],[]
    
    
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
    r_min, r_max, theta_min, theta_max = prm.R, prm.R_ext, prm.theta_min, prm .theta_max
    
    dr = lambda nx: abs(r_max-r_min)/(nx-1)
    dtheta = lambda ny: abs(theta_max-theta_min)/(ny-1)
    tab=np.array([dr(i)*dtheta(i) for i in noeuds_err])
    print(tab)
   
    graphique_convergence_erreurs(tab,erreurs,'dr')
   
def propagation():
    ### Résolution du problème avec paramètres initaux 
    prm = Parametres()
    
    errL1=[]
    errL2=[]
    errLinf=[]
    nb_noeuds=25
    rayons=[2.0231333123933544, 2.1501147686017514, 2.6180125908349163, 1.4993313856327224, 2.269093789712684, 4.157846502182325, 1.616644476288664, 2.246662270928322, 1.9074518519229011, 1.5413922316137434, 1.6668577303555203, 1.6191002686384126, 2.346189700771556, 1.2638109736007561, 1.9825601523707768, 1.5629003497264278, 2.092999972866811, 2.292374944563457, 1.9593470670702164, 1.5654272765937725, 1.7783825323272433, 2.0719612396753733, 1.8273061377206163, 1.3873159052083692, 1.9583660726271934, 1.4234258184742314, 1.655274147749532, 1.5110464445229965, 2.6940702299651127, 2.217622905390624, 1.604940267270745, 2.1506511987267087, 1.361019892370793, 1.6779654136867348, 1.581163965836162, 1.991149308132889, 1.928485359689747, 1.4390761241122612, 2.347838618833941, 2.1479306335961446, 2.001867405341038, 4.153517819236928, 1.5014329172594065, 2.129073306072839, 1.9661342728452769, 2.5898396884865456, 3.005929567717712, 1.7071871276949184, 2.17804212938698, 1.7237214433128836, 1.455085777263597, 3.0296242115135765, 1.6516964673450678, 2.279817304651554, 3.1803767966455236, 1.4520865987917615, 3.154855230504548, 2.0795599521331725, 1.5731719534248194, 2.3602007850556275, 1.7984601799615474, 2.502329222581122, 1.581570417321334, 1.7671459009972545, 1.6742796201758097, 1.8783540764248277, 2.0316838400560684, 2.0643657967510816, 2.539425611213262, 1.9239864793330868, 2.075767890430878, 1.9670268601069965, 1.7932132470474427, 2.3641822288581515, 2.1776634444180134, 2.1300522423617787, 1.7948060061943316, 2.9371645976313188, 1.6157448517518804, 1.565541549155506, 2.116553814330181, 2.207368301628568, 3.292790971598566, 2.4826638849113216, 1.5978263707335998, 1.6866958863295172, 1.6874273423156674, 2.32975924006728, 1.7499048067768326, 1.8420862035496277, 1.6040407479362908, 2.1248677572729293, 1.2389849217698106, 2.3667264375363994, 2.036781697013902, 2.1426316664840694, 2.2546876118047514, 1.9165839757884437, 1.3877151749379961, 1.987476254410119]
    Resultats=[]
    for rayon in rayons: 
        prm.R=rayon
        print("Calculating for r = ", rayon)
        prm.nx = nb_noeuds
        prm.ny = nb_noeuds

        # on recalcule les caractéristiques de la situation avec la mdf 
        r_mesh, theta_mesh, vecteur_psis = f.mdf(params=prm)
        psi_mdf_mesh = f.arrange_mesh(vecteur_psis, prm.nx, prm.ny) # valeurs de psi calculées par mdf sur maillage 
        vr, vtheta = f.vitesses(vecteur_psis, prm) 
        vr_mesh, vtheta_mesh = f.arrange_mesh(vr, prm.nx, prm.ny), f.arrange_mesh(vtheta, prm.nx, prm.ny) 
        # on calcule les solutions analytiques associées 
        # psi_analytique_mesh = f.psi_ref_mesh(prm) # valeurs de psi analytique sur le maillage 
        # vr_mesh_ref, vtheta_mesh_ref = f.vr_ref_mesh(prm), f.vtheta_ref_mesh(prm) # valeurs de vitesse analytique sur maillage 

        # On utilise la norme de la vitesse pour calculer l'erreur associée, pour générer les erreurs, on n'a pas besoin de convertir en cartésien 
        # vitesses_ref = np.sqrt(vr_mesh_ref**2 + vtheta_mesh_ref**2) # normes de la vitesse analytique 
        # vitesses_mdf = np.sqrt(vr_mesh**2 + vtheta_mesh**2) # normes de la vitesse par mdf 
        Resultats.append(psi_mdf_mesh)
        # # On evalue l'erreur 
        # domaine = [i for i in range(prm.nx)]
        # errL1.append(erreur_L1(domaine, psi_mdf_mesh, psi_analytique_mesh))
        # errL2.append(erreur_L2(domaine, psi_mdf_mesh, psi_analytique_mesh))
        # errLinf.append(erreur_Linf(domaine, psi_mdf_mesh, psi_analytique_mesh))
    print(Resultats)
    #PST tire de propagation des incertitude
    # traitement des résultats
    res=[Resultats[i][3][3] for i in range(len(Resultats))]
    # Calculer la moyenne et l'écart type
    moyenne = np.mean(res)
    ecart_type = np.std(res)
    median = np.median(res)

    print("Moyenne :", moyenne)
    print("Écart type :", ecart_type)
    print("Medianne :", median)

    # Calculer la CDF de vos résultats de sortie
    sorted_srq = np.sort(res)
    cdf = np.arange(1, len(res) + 1) / len(res)

    # Tracer la CDF
    plt.plot(sorted_srq, cdf)
    plt.xlabel('Valeur de sortie')
    plt.ylabel('Probabilité cumulative')
    plt.title('CDF de la sortie (SRQ)')
    plt.grid(True)
    plt.savefig("CDF_de_la_sortie_(SRQ)")
    plt.show()
    
if __name__=="__main__": 
    main()
    