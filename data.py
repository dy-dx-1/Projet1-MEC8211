# -*- coding: utf-8 -*-
"""
Created on Thu Feb 1 11:50:58 2024

@author: alsip
"""

class Data:

    def __init__(self, Ntt=5):
        """
        Classe représentant les données du problème.

        Parameters
        ----------
        Ntt : int, optional
            Nombre de points dans le domaine, by default 5.

        """
        # Variables modifiables par l'utilisateur (transférées dans le script principal peut-être?)
        self._Ntt = Ntt
        self.stationnaire = True

        # Constantes
        self.Deff = 10e-10
        self.unsurDeff = 1 / self.Deff
        self.L = 0.5
        self.Ce = 12

        self.dr = self.L / (self.Ntt - 1)
        self.unsurdr = 1 / self.dr

        # Si S n'est pas constant, décommentez les lignes suivantes
        self.S = 8 * 10e-9
        self.k = 4 * 10e-9
        self.const = True

        # Valeurs pour la boucle temporelle
        self.dt = 0.1  # Pas précisé
        self.crit = 1e-10
        self.itermax = 1000

    @property
    def Ntt(self):
        """
        Accesseur pour Ntt.

        Returns
        -------
        int
            Nombre de points dans le domaine.

        """
        return self._Ntt

    @Ntt.setter
    def Ntt(self, value):
        """
        Modificateur pour Ntt.

        Parameters
        ----------
        value : int
            Nouvelle valeur pour Ntt.

        """
        self._Ntt = value
        self.update_dr()  # Appeler update_dr lorsque Ntt est modifié

    def update_dr(self):
        """
        Met à jour dr en fonction de la nouvelle valeur de Ntt.

        """
        self.dr = self.L / (self.Ntt - 1)
        self.unsurdr = 1 / self.dr
