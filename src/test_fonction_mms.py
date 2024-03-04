import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

r,t = sp.symbols('r t')

R = 0.5  # Diamètre du cylindre [m]
D = 10**(-10) # coeff diffusion effective 
S = 8*(10**(-9)) # terme source si constant 
k = 4*(10**(-9)) # constante de réaction si réaction du premier ordre 
C_ext = 12 # Concentration à l'extérieur
nb_annees = 100
nb_jours = nb_annees*365.25
t_sim = int(nb_jours*24*60*60) # temps de simulation

C_MMS = C_ext + t*(1-r**2/(R**2))*sp.cos(r)/t_sim
print(sp.latex(C_MMS))

dC_MMS_r = sp.diff(C_MMS,r)
print("derive r",sp.latex(dC_MMS_r))
ddC_MMS_r = sp.diff(dC_MMS_r,r)
print("double derivee r",sp.latex(ddC_MMS_r))
dC_MMS_t = sp.diff(C_MMS,t)
print("derive t",sp.latex(dC_MMS_t))