import unittest

import numpy as np
from src.Controleur.controleur import *
from src.environnement import Environnement
from src.Robot.robot import Adaptateur_simule


class TestControleur(unittest.TestCase):
    def setUp(self):
        self.env = Environnement(70, 55, 1)
        self.rob = Adaptateur_simule("Rob", 10, 15, 5, 7, 8)
        self.controleur = Controler()

    def test_setStrategieCarre(self):
        Controler.setStrategieCarre(self.controleur, self.rob, 20)
        self.assertAlmostEqual(self.rob.x, 10)
        self.assertAlmostEqual(self.rob.y, 15)

    def test_setStrategieArretMur(self):
        Controler.setStrategieArretMur(self.controleur, self.rob, 20 ,self.env)
        self.assertGreaterEqual(20,self.rob.capteurDistance(self.env))
