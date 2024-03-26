import unittest

from src.Controleur.controleur import *
from src.environnement import Environnement
from src.Robot.robot import Adaptateur_simule


class TestControleur(unittest.TestCase):
    def setUp(self):
        self.env = Environnement(70, 55, 1)
        self.rob = Adaptateur_simule("Rob", 10, 15, 5, 7, 8, self.env)
        self.controleur = Controler()
        self.carre = setStrategieCarre(self.rob, 30)

    def TestlanStrategie(self):
        self.controleur.lancerStrategie(self.carre)
        self.assertEqual(self.controleur.strategie, 1)
        self.assertEqual(self.controleur.strat_en_cour, self.carre)