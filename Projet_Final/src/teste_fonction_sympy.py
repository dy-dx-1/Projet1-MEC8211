import sympy as sp


# Définition des symboles
r, theta, R_ext, U_inf, R = sp.symbols('r theta R_ext U_inf R')

# Définition de la fonction psi
psi = sp.cos(2*sp.pi*r/R_ext) * sp.sin(theta) * U_inf * R_ext * (1 - R**2/r**2)

# Affichage de la fonction psi
print("𝜓(r, θ) = ", sp.latex(psi))

# Calculer les dérivées partielles de psi
d_psi_dr = sp.diff(psi, r)
d_psi_dtheta = sp.diff(psi, theta)

# Calculer les dérivées secondes
d2_psi_dr2 = sp.diff(d_psi_dr, r)
d2_psi_dtheta2 = sp.diff(d_psi_dtheta, theta)
d2_psi_drdtheta = sp.diff(d_psi_dr, theta)

# Définir la fonction L(r, theta)
L = d2_psi_dr2  + 1 / r * d_psi_dr + 1 / r**2 * d2_psi_dtheta2 

# Afficher L(r, theta)
print("L(r, theta) =", L)
