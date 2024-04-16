import fonctions as f 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.interpolate import interp1d

from  graphique_convergence import  graphique_convergence_erreurs,erreur_L1,erreur_L2,erreur_Linf

class Parametres():
    u_inf = 1 
    R = 1 
    R_ext = 5 
    
    theta_min = 0 
    theta_max = 2 * np.pi 

    nx = 15
    ny = 30

#fonction fiter
prm=Parametres()
fiter_noeud=[20,22,24]

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

print(ordreCl,ordreCd)



#Prediction Cd
x=[i for i in range(len(u_infs))]
y_up=[E_Cd+incertitudes_Cd/2 for j in range(len(E_Cd))]
y_mid=E_Cd
y_down=[E_Cd-incertitudes_Cd/2 for j in range(len(E_Cd))]


f_up = interp1d(x, y_up, kind='linear')
f_mid = interp1d(x, y_mid, kind='linear')
f_down = interp1d(x, y_down, kind='linear')

predi_CD=[f_mid(100),f_up(100)-f_down(100)]
#Prediction Cl
y_up=[E_Cl+incertitudes_Cl/2 for j in range(len(E_Cl))]
y_mid=E_Cl
y_down=[E_Cl-incertitudes_Cl/2 for j in range(len(E_Cl))]


f_up = interp1d(x, y_up, kind='linear')
f_mid = interp1d(x, y_mid, kind='linear')
f_down = interp1d(x, y_down, kind='linear')

predi_Cl=[f_mid(100),f_up(100)-f_down(100)]