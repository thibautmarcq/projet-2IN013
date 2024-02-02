import unittest
import numpy as np

from Code.environnement import Environnement

class TestEnvironnement(unittest.TestCase):
    def setUp(self):
        self.env = Environnement(40,30,5)


    def test_constructeur(self):
        self.assertEqual(self.env.width, 40)
        self.assertEqual(self.env.height, 30)
        self.assertIsInstance(self.env.matrice, np.ndarray)
        self.assertEqual(len(self.env.robots), 0)
        self.assertEqual(self.env.scale, 5)
        

    # def test_addRobot(self):
    #     pass

    # def test_addObstacle(self):
    #     pass

    # def test_detect_obs(self):
    #     pass

    # def test_affiche(self):
    #     # Methode non définie dans Environnement
    #     pass