# python3 -m unittest Test/test_obs.py -v

import unittest

from Code.obstacle import Obstacle
from Code.environnement import Environnement

class TestObstacle(unittest.TestCase):
    def setUp(self) :
        self.env1 = Environnement(30, 30, 1)
        self.obs = Obstacle("Pierre", [(14,5), (24,8), (24,12.2), (14,12.5)], self.env1)
        # self.obs = Obstacle("Coeur", [(9,2), (17,9), (15,12), (12,12), (9,10), (6,12), (3,12), (2,9)], self.env1)

    def test_attributs(self):
        self.assertEqual(self.obs.nom, "Pierre")
        self.assertEqual(self.obs.lstPoints, [(14,5), (24,8), (24,12.2), (14,12.5)])
        self.assertTrue(self.obs.env==self.env1)

    