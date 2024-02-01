import unittest

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

    def test_setVitesse(self):
        self.rob.setVitesse(12)
        self.assertEqual(self.rob.vitesse, 12)