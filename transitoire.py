import numpy as np 
import matplotlib.pyplot as plt 

def main():
    ro = 0.5 
    D = 10**(-10) # coeff diffusion effective 
    S = 8*(10**(-9)) 
    C_ext = 12 

    N = 5 
    dt = 500
    t = 0 # temps initial 
    nb_jours = 1000
    t_sim = nb_jours*60*60*24 # temps de simulation 
    domaine = np.linspace(0, ro, N)
    dr = ro/(N-1) 

    ## Coefficients associés aux noeuds 
    alpha = lambda ri: np.true_divide(-D, np.square(dr)) - np.true_divide(D, dr*ri) # ci+1
    beta = lambda ri: np.true_divide(1,dt) + np.true_divide(2*D, dr**2) + np.true_divide(D, ri*dr)
    zeta = np.true_divide(-D, dr**2)

    ### conditions initiales 
    C = np.zeros(N) 
    Ci = 0 
    for i in range(N): C[i]=Ci 

    while t<=t_sim: 
        A = np.zeros((N, N))
        B = np.zeros((N, 1))
        ### Construction centre de la matrice 
        for i in range(1, N-1): # descente verticale (sur les lignes)
            r = domaine[i]
            A[i, i+1] = alpha(r)
            A[i, i] = beta(r) 
            A[i, i-1] = zeta 
            B[i, 0] = np.true_divide(C[i], dt) - S # le C indexé correspond au C au temps t, vu qu'on calcule pour le t+1 
        ### Ajout des conditions limites 
        ## Neumann 
        A[0, 0] = -1 
        A[0, 1] = 1 ## mntn derivee avant ordre 1 
        B[0, 0] = 0 
        ## Dirichlet 
        A[N-1, N-1] = 1 
        B[N-1, 0] = C_ext 
        ### Solution du système 
        C_new = np.linalg.solve(A, B) # nouvelles valeurs donc on peut passer à la prochaine itération 
        C =np.copy(C_new)
        t+=dt

    # Affichage 
    plt.plot(domaine, C, ".-") 
    C_exact = np.true_divide(S,4*D)*np.square(ro)*(np.square(np.divide(domaine, ro))-1)+C_ext
    plt.plot(domaine, C_exact) # analytique 
    plt.show() 
              

if __name__ == "__main__":
    main() 