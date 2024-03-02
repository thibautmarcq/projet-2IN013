# python3 -m unittest Test/test_obs.py -v

import unittest

from Code.environnement import Environnement
from Code.obstacle import Obstacle


class TestObstacle(unittest.TestCase):
    def setUp(self) :
        self.obs1 = Obstacle("Pierre", [(14,5), (24,8), (24,12.2), (14,12.5)])
        self.obs2 = Obstacle("Caillou",[(4, 26), (6, 24), (8, 26), (10, 24), (10, 20), (8, 22), (6, 20), (4, 22)])
        self.obs3 = Obstacle("Roche", [(0, 0)])
        self.obs4 = Obstacle("Montagne", [(-1, -1), (0, 0), (1, 1), (0, 0)])
        # self.obs = Obstacle("Coeur", [(9,2), (17,9), (15,12), (12,12), (9,10), (6,12), (3,12), (2,9)], self.env1)

    def test_attributs(self):
        self.assertEqual(self.obs1.nom, "Pierre")
        self.assertEqual(self.obs1.lstPoints, [(14,5), (24,8), (24,12.2), (14,12.5)])
        self.assertEqual(self.obs2.nom, "Caillou")
        self.assertEqual(self.obs2.lstPoints, [(4, 26), (6, 24), (8, 26), (10, 24), (10, 20), (8, 22), (6, 20), (4, 22)])
        self.assertEqual(self.obs3.nom, "Roche")
        self.assertEqual(self.obs3.lstPoints, [(0, 0)])
        self.assertEqual(self.obs4.nom, "Montagne")
        self.assertEqual(self.obs4.lstPoints, [(-1, -1), (0, 0), (1, 1), (0, 0)])
        
