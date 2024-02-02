import numpy as np 
import matplotlib.pyplot as plt 

def main():
    D = 0 
    dt = 0
    dr = 0 
    S = 0 
    
    N = 5 
    t = 0 # temps initial 
    t_sim = 100 # temps de simulation 

    ### conditions initiales 
    C = np.zeros(N) 
    Ci = 0 
    for i in range(N): C[i]=Ci 

    while t<=t_sim: 
        A = np.zeros(N, N)
        B = np.zeros(N, 1)
        for i in range(1, N): 
            ### Construction centre de la matrice 
            pass 


     

if __name__ == "__main__":
    main() 