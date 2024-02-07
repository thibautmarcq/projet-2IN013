# python3 -m unittest Test/test_obs.py -v

import unittest

from Code.obstacle import Obstacle 

class TestObstacle(unittest.TestCase):
    def setUp(self) :
        self.obs = Obstacle("Pierre", 20, 30)

    def test_coords(self):
        self.assertEqual(self.obs.x, 20)
        self.assertEqual(self.obs.y, 30)
        self.assertEqual(self.obs.nom, "Pierre" )

    