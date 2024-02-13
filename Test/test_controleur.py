import unittest
import numpy as np

from Code.Controleur.controleur import StrategieAvancer
from Code.robot import Robot

class TestControleur(unittest.TestCase):
    def setUp(self):
        self.rob = Robot("Rob", 10, 15, 5, 7, 8)
        self.stratAvancer = StrategieAvancer(10, self.rob)

    def test_controleur(self):
        self.assertEqual(self.stratAvancer.parcouru, 0)
        self.assertEqual(self.stratAvancer.distance, 10)

    def test_anvancer_step(self):
        self.stratAvancer.step()
        self.assertEqual(self.stratAvancer.parcouru, 1)

    def test_avancer_stop(self):
        while self.stratAvancer.stop() != 0:
            self.stratAvancer.step()
        self.assertGreaterEqual(self.stratAvancer.parcouru, 10)