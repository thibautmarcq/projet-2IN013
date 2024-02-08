# python3 -m unittest Test/test_robot.py -v

import unittest
import math 

from Code.robot import Robot

class TestRobot(unittest.TestCase):
    def setUp(self) :
        self.rob = Robot("Rob", 10, 15, 5, 7, 8) 
    
    def test_constructeur(self):
        self.assertEqual(self.rob.nom, "Rob")
        self.assertEqual(self.rob.x, 10)
        self.assertEqual(self.rob.y, 15)
        self.assertEqual(self.rob.width, 5)
        self.assertEqual(self.rob.length, 7)
        self.assertEqual(self.rob.vitesse, 0)
        self.assertEqual(self.rob.direction, (0,-1))
        self.assertEqual(self.rob.rayonRoue, 8)

    def test_setVitesse(self):
        self.rob.setVitesse(12)
        self.assertEqual(self.rob.vitesse, 12)

    def test_rotation(self):
        self.rob.rotation()
        dirx,diry = self.rob.direction
        self.assertAlmostEqual(dirx, 0)
        self.assertAlmostEqual(diry, -1)

    def test_avancer(self):
        self.rob.avancerDirection()
        self.assertEqual(self.rob.x, 10)
        self.assertEqual(self.rob.y, 7)

    def test_reculer(self):
        self.rob.setVitesse(8)
        self.rob.reculerDirection()
        self.assertEqual(self.rob.x, 10)
        self.assertEqual(self.rob.y, 23)

    
