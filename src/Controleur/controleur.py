from logging import getLogger
from threading import Thread
from time import sleep

from src import TIC_CONTROLEUR


class Controler:

    def __init__(self):
        """
        Constructeur de la classe Controler
        """
        self.logger = getLogger(self.__class__.__name__)
        self.strat_en_cour = None
        self.strategie = 0
        self.Running = True
        t = Thread(target=self.mainControleur, daemon=True)
        t.start()

    def mainControleur(self):
        """
        Main du controleur
        """
        while self.Running:
            if self.strategie:
                if not self.strat_en_cour.stop():
                    self.strat_en_cour.step()
                else:
                    self.strategie = 0
                    self.strat_en_cour.robA.setVitAngA(0)
                    self.strat_en_cour.robA.run = False
                    self.strat_en_cour = None
            sleep(TIC_CONTROLEUR)

    def lancerStrategie(self, strat):
        """ Méthode qui permet de lancer une stratégie
            :param strat: la stratégie que l'on veut lancer
        """
        if self.strategie:
            self.logger.error("Impossible de lancer la stratégie tant que le controleur n'est pas libre")
        self.strat_en_cour = strat
        self.strategie = 1
        self.strat_en_cour.start()