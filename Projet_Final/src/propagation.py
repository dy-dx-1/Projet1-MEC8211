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


if __name__=="__main__": 
    propagation()