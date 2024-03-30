from unittest import TestCase

from src.Controleur.controleur import *
from src.Controleur.strategies import setStrategieCarre
from src.environnement import Environnement
from src.Robot.robot import Adaptateur_simule


class TestControleur(TestCase):
    def setUp(self):
        self.env = Environnement(70, 55, 1)
        self.rob = Adaptateur_simule("Rob", 10, 15, 5, 7, 8, self.env, "red")
        self.controleur = Controler()
        self.carre = setStrategieCarre(self.rob, 30)

    def test_lancerStrategie(self):
        self.controleur.lancerStrategie(self.carre)
        self.assertEqual(self.controleur.strategie, 1)
        self.assertEqual(self.controleur.strat_en_cour, self.carre)