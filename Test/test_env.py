# python3 -m unittest Test/test_env.py -v

import unittest
import numpy as np

from Code.environnement import Environnement
from Code.robot import Robot

class TestEnvironnement(unittest.TestCase):
    def setUp(self):
        self.env = Environnement(40,30,5)


    def test_constructeur(self):
        self.assertEqual(self.env.width, 40)
        self.assertEqual(self.env.height, 30)
        self.assertIsInstance(self.env.matrice, np.ndarray)
        self.assertEqual(len(self.env.robots), 0)
        self.assertEqual(self.env.scale, 5)
        

    def test_createRobot(self):
        self.assertEqual(len(self.env.robots), 0)
        self.env.createRobot("Bobby", 18, 14.5, 5, 8, 0)
        self.assertEqual(len(self.env.robots), 1)
        self.assertIsInstance(self.env.robots[0], Robot)
        # Ajouter test après condition dehors environnement

    def test_addObstacle(self):
        self.env.addObstacle("Roger")
        self.assertTrue(2 in self.env.matrice)
        
    # def test_detect_obs(self):
    #     pass

    # def test_affiche(self):
    #     # Methode non définie dans Environnement
    #     pass