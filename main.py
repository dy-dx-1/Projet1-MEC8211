import numpy as np 
import matplotlib.pyplot as plt 

def main():
    ro = 0
    D = 0 
    dt = 0
    dr = 0 
    S = 0 
    C_ext = 0 

    N = 5 
    t = 0 # temps initial 
    t_sim = 100 # temps de simulation 

    ## Coefficients associés aux noeuds 
    alpha = lambda ri: np.true_divide(-D/np.square(dr)) - np.true_divide(D, dr*ri) # ci+1
    beta = lambda ri: np.true_divide(1/dt) + np.true_divide(2*D, dr**2) + np.true_divide(D, ri*dr)
    zeta = np.true_divide(-D, dr**2)

    ### conditions initiales & domaine 
    domaine = np.linspace(0, ro, N)
    C = np.zeros(N) 
    Ci = 0 
    for i in range(N): C[i]=Ci 

    while t<=t_sim: 
        A = np.zeros(N, N)
        B = np.zeros(N, 1)
        ### Construction centre de la matrice 
        for i in range(1, N): # descente verticale (sur les lignes)
            r = domaine[i]
            A[i, i+1] = alpha(r)
            A[i, i] = beta(r) 
            A[i, i-1] = zeta 
            B[i, 0] = np.true_divide(C[i], dr) - S # le C indexé correspond au C au temps t, vu qu'on calcule pour le t+1 
        ### Ajout des conditions limites 
        ## Neumann 
        A[0, 0] = -1 
        A[0, 1] = 1 ## mntn derivee avant ordre 1 
        B[0, 0] = 0 
        ## Dirichlet 
        A[N, N] = 1 
        B[N, 0] = C_ext 
        ### Solution du système 
        C = np.linalg.solve(A, B) 
        
        



     

if __name__ == "__main__":
    main() 