# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:50:58 2024

@author: alsip
"""


class Data():

    def __init__(self,Ntt=5):
        #variables modifiable de l'utilisateur (transfere sur main may be ?)
        self._Ntt = Ntt
        self.const = True
        
        #Constantes
        self.Deff = 10e-10
        self.L = 0.5
        self.Ce = 12
        
        
        
        self.dx=self.L/self.Ntt
        self.unsurdx=1/self.dx
        
        #Si S n'est pas constant decomentez les lignes suivantes
        self.S = 8*10e-9
        self.k = 4*10e-9
        self.const = True
        
        #Valeur pour la boucle temporelle
        self.dt=1e-5 #pas précisé
        self.itermax=1000
        
    @property
    def Ntt(self):
        return self._Ntt
    @Ntt.setter
    def Ntt(self, value):
       self._Ntt = value
       self.update_dx()  # Appeler update_dx lorsque Ntt est modifié
    
    def update_dx(self):
        # Mise à jour de dx en fonction de la nouvelle valeur de Ntt
        self.dx = self.L / self.Ntt
        self.unsurdx = 1 / self.dx
