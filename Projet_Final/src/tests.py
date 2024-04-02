import numpy as np 
import fonctions as f 

class Test:

    def test_maillage(self): 
        """Test vérifiant que la génération de maille fonctionne"""
        coord_r = [[0, 1, 2, 3], 
                   [0, 1, 2, 3], 
                   [0, 1, 2, 3]] 
        coord_theta = [[10, 10, 10, 10], 
                       [5, 5, 5, 5], 
                       [0, 0, 0, 0]] 
        r_test, theta_test = f.gen_maille(r_min = 0, r_max = 3, theta_min = 0, theta_max = 10, nx = 4, ny = 3)
        r_check = abs(r_test-coord_r)<1e-3
        theta_check = abs(theta_test-coord_theta)<1e-3
        assert all([r_check.all(), theta_check.all()])

    def test_convert_indices(self): 
        """ Test vérifiant que la convertion d'indices marche bien"""
        # prenons les points suivants, format (i, j, k), nx = 4
        p1 = (2, 0, 2) 
        p2 = (1, 1, 5) 
        p3 = (3, 2, 11) 

        # test de i 
        assert abs(p1[0]-f.convert_indices(nx=4, i=None, j=p1[1], k=p1[2]))<1e-6
        # test de j 
        assert abs(p2[1]-f.convert_indices(nx=4, i=p2[0], j=None, k=p2[2]))<1e-6
        # test de k 
        assert abs(p3[2]-f.convert_indices(nx=4, i=p3[0], j=p3[1], k=None))<1e-6
        # test d'erreur 
        assert (f.convert_indices(nx=4, i=1, j=2, k=3) is None)

    def test_central_shape(self): 
        """Test vérifiant que la fonction de gen_central_values ne génére pas de conditions limites"""
        maille_test1 = f.gen_central_values(k=9, nx=4, ny=4, rk=1, dr=1, dtheta=1)
        maille_test2 = f.gen_central_values(k=14, nx=4, ny=6, rk=1, dr=1, dtheta=1)
        maille_test3 = f.gen_central_values(k=8, nx=6, ny=3, rk=1, dr=1, dtheta=1) 
        # Verif que toutes les colonnes des bords sont nulles 
        assert all([ (maille_test1[0] == 0).all(),
                     (maille_test1[-1] == 0).all(),
                     (maille_test1[:,0] == 0).all(),
                     (maille_test1[:,1] == 0).all() ]) 
        assert all([ (maille_test2[0] == 0).all(),
                     (maille_test2[-1] == 0).all(),
                     (maille_test2[:,0] == 0).all(),
                     (maille_test2[:,1] == 0).all() ]) 
        assert all([ (maille_test3[0] == 0).all(),
                     (maille_test3[-1] == 0).all(),
                     (maille_test3[:,0] == 0).all(),
                     (maille_test3[:,1] == 0).all() ]) 
        
    def test_integral(self): 
        """ 
        Test de la fonction d'integration. On vérifie qu'elle est capable d'intégrer avec 2 fonctions 
        dont la solution analytique est simple à obtenir. 
        """
        dom = np.linspace(-5, 5, 10000)  # domaine subdivisé en 50 pts donc 49 sous intervalles 
        y1 = np.sin(dom) 
        y2 = np.cos(dom)  

        check1 = abs(f.integrale(dom, y1)-0)<1e-2
        check2 = abs(f.integrale(dom, y2)-(2*np.sin(5)))<1e-2 
        
        assert all([check1, check2])

    def test_deriv_by_coeff(self): 
        """
        Test de la fonction derivant les valeurs d'un maillage par rapport à une direction donnée 
        """
        # Un test simple pour vérifier un aspect de la fonction serait de dériver des coeff constants dans la direction de dérivation 
        #a_ref =  [[1,1,1],
        #          [2,2,2],
        #          [3,3,3]]   # exemple des valeurs de noeuds constantes sur la direction r 
        #b_ref =  [[1,2,3],
        #          [1,2,3],
        #          [1,2,3]]   # exemple des valeurs de noeuds constantes sur la direction theta
        a_ref = [1,1,1, 2,2,2, 3,3,3]
        b_ref = [1,2,3, 1,2,3, 1,2,3]
        a = f.deriv_by_coeff(a_ref, 'r', nx=3, delta = 0.1) # le delta n'est pas important 
        b = f.deriv_by_coeff(b_ref, 'theta', nx=3, delta = 0.1) # le delta n'est pas important 
        r_check = a==np.zeros(9)
        assert r_check.all() 
        theta_check = b==np.zeros(9) 
        assert theta_check.all() 
        # finalment verifions qu'on n'a pas zero dans l'autre direction 
        c =  f.deriv_by_coeff(a_ref, 'theta', nx=3, delta = 0.1)
        d = f.deriv_by_coeff(b_ref, 'r', nx=3, delta = 0.1)
        r_check = c==np.zeros(9)
        assert not r_check.all() 
        theta_check = d==np.zeros(9) 
        assert not theta_check.all() 

    def test_arrange_mesh(self): 
        """ 
        Test de la fonction explicitant un array 1D des valeurs associées à des noeuds 'k' en son maillage 2D de la forme: 
        k=0  k=1    k=2    ... k=nx-1 
        k=nx k=nx+1 k=nx+2 ... k=2nx-1 
        ...  ...    ...    ... ...
        ...  ...    ...    ... k = N-1 
        Où,
        nx: nombre de valeurs horizontales,
        ny: nombre de valeurs verticales, 
        N=nx*ny: Nombre de noeuds au total 
        """
        # testons 3 cas, nx>ny, ny>nx et nx=ny 
        # Premier cas, nx=5, ny=3 
        a = [[0,   1,  2,  3,  4], 
             [5,   6,  7,  8,  9], 
             [10, 11, 12, 13, 14]]
        a_test = f.arrange_mesh(np.arange(15), nx=5, ny=3)
        check = a==a_test
        assert check.all() 
        # Deuxieme cas, nx=2, ny=4
        b = [[0,   1], 
             [2,   3], 
             [4,   5],
             [6,   7]]
        b_test = f.arrange_mesh(np.arange(8), nx=2, ny=4)
        check = b==b_test
        assert check.all() 
        # Troisieme cas, nx=3, ny=3 ET un vecteur de valeurs k qui != les indices des noeuds (on devrait avoir la bonne shape avec les valeurs placées)
        c = [[3,   4,  5], 
             [6,   0,  8], 
             [9,  11,  20]]
        valeurs_test = [3,4,5,6,0,8,9,11,20]
        c_test = f.arrange_mesh(valeurs_test, nx=3, ny=3)
        check = c==c_test
        assert check.all() 

    def test_conditions_limites(self):
        """Test vérifiant que les solutions répondent bien à nos conditions limites """
        class Parametres():
            u_inf = 1 
            R = 1 
            R_ext = 5 
            
            theta_min = 0 
            theta_max = 2 * np.pi 

            nx = 15
            ny = 20
        prm = Parametres()
        noeuds, res, solutions = f.mdf(params=prm)
        psi_mesh = f.arrange_mesh(solutions, prm.nx, prm.ny) 
        print(psi_mesh)
        discretisation_theta = np.linspace(prm.theta_max, prm.theta_min, prm.ny) # l'ordre est important pour match maillage 
        ref_psi_droit = prm.u_inf*prm.R_ext*np.sin(discretisation_theta)*(1-np.square(prm.R/prm.R_ext))
        # Maintenant qu'on a les valeurs de psi arrangés sur la maille de notre domaine il est simple de vérifier les conditions
        check_gauche = psi_mesh[:,0] < 1e-10
        check_bas = psi_mesh[prm.ny-1,:] < 1e-10 
        check_haut = psi_mesh[0, :] < 1e-10 
        check_droit = abs(psi_mesh[:,prm.nx-1] - ref_psi_droit)<1e-6
        assert check_gauche.all() 
        assert check_bas.all() 
        assert check_haut.all() 
        assert check_droit.all() 

    def test_resultats_mdf(self):
        """Test vérifiant que la solutions repond a celle exacte"""
        class Parametres():
            u_inf = 1 
            R = 1 
            R_ext = 5 
            
            theta_min = 0 
            theta_max = 2 * np.pi 

            nx = 15
            ny = 20
        prm = Parametres()
        r, theta, solutions = f.mdf(params=prm)
        psi_mesh = f.arrange_mesh(solutions, prm.nx, prm.ny) 
        psi_mesh_ref = f.psi_ref_mesh(prm) 
        assert (abs(psi_mesh-psi_mesh_ref)<1e-2).all() 