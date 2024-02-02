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
        self.assertEqual(self.rob.vitesse, 8)
        self.assertEqual(self.rob.direction, (0,-1))

    def test_setVitesse(self):
        self.rob.setVitesse(12)
        self.assertEqual(self.rob.vitesse, 12)

    def test_rotation(self):
        self.rob.rotation(math.pi/6)
        dirx,diry = self.rob.direction
        self.assertAlmostEqual(dirx, 1.0/2)
        self.assertAlmostEqual(diry, -math.sqrt(3)/2.0)

    def test_avancer(self):
        self.rob.avancerDirection()
        self.assertEqual(self.rob.x, 10)
        self.assertEqual(self.rob.y, 7)
    
