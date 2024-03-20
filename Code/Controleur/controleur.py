import logging
import time
from threading import Thread

from Code.outil import *
from Code.constantes import *
from Code.Controleur.Strategies import *


class Controler:

    def __init__(self):
        """
        Constructeur de la classe Controler
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.strat_en_cour = None
        self.strategie = 0
        self.Running = True
        t = Thread(target=self.mainControleur, daemon=True)
        t.start()

    def mainControleur(self):
        while self.Running:
            if self.strategie:
                if not self.strat_en_cour.stop():
                    self.strat_en_cour.step()
                else:
                    self.strategie = 0
                    self.strat_en_cour.getRob().setVitAngA(0)
                    self.strat_en_cour = None
            time.sleep(TIC_CONTROLEUR)

    def setStrategie(self, strat):
        """
        Méthode qui permet de lancer une stratégie
        :param strat: la stratégie que l'on veut lancer
        """
        if self.strategie:
            self.logger.error("Impossible de lancer la stratégie tant que le controleur n'est pas libre")
        self.strat_en_cour = strat
        self.strategie = 1
        self.strat_en_cour.start()

    def lancerStrategie(self, strat) : 
        self.setStrategie(strat)






