# python3 -m unittest Test/test_robot.py -v

import unittest
import math 

from src.Robot.robot import Robot
from src.environnement import Environnement

class TestRobot(unittest.TestCase):
    def setUp(self) :
        self.rob = Robot("Rob", 10, 15, 5, 7, 8) 
    
    def test_constructeur(self):
        self.assertEqual(self.rob.nom, "Rob")
        self.assertEqual(self.rob.x, 10)
        self.assertEqual(self.rob.y, 15)
        self.assertEqual(self.rob.width, 5)
        self.assertEqual(self.rob.length, 7)
        self.assertEqual(self.rob.direction, (0,-1))
        self.assertEqual(self.rob.rayonRoue, 8)
        self.assertEqual(self.rob.vitAngD, 0)
        self.assertEqual(self.rob.vitAngG, 0)

    # def test_refresh(self):
        
    def test_setVitAngG(self):
        self.rob.setVitAngG(5)
        self.assertEqual(self.rob.vitAngG,5)
        self.rob.setVitAngG(-7)
        self.assertEqual(self.rob.vitAngG,-7)
        self.rob.setVitAngG(0)
        self.assertEqual(self.rob.vitAngG,0)

    def test_setVitAngD(self):
        self.rob.setVitAngD(5)
        self.assertEqual(self.rob.vitAngD,5)
        self.rob.setVitAngD(-7)
        self.assertEqual(self.rob.vitAngD,-7)
        self.rob.setVitAngD(0)
        self.assertEqual(self.rob.vitAngD,0)

    def test_changeVitAngG(self):
        self.rob.changeVitAngG(5)
        self.assertEqual(self.rob.vitAngG,5)
        self.rob.changeVitAngG(2)
        self.assertEqual(self.rob.vitAngG,7)
        self.rob.changeVitAngG(-7)
        self.assertEqual(self.rob.vitAngG,0)
    
    def test_changeVitAngD(self):
        self.rob.changeVitAngD(5)
        self.assertEqual(self.rob.vitAngD,5)
        self.rob.changeVitAngD(2)
        self.assertEqual(self.rob.vitAngD,7)
        self.rob.changeVitAngD(-7)
        self.assertEqual(self.rob.vitAngD,0)

    def test_changeVitAng(self):
        self.rob.changeVitAng(5)
        self.assertEqual(self.rob.vitAngG,5)
        self.assertEqual(self.rob.vitAngD,5)
        self.rob.changeVitAng(-5)
        self.assertEqual(self.rob.vitAngG,0)
        self.assertEqual(self.rob.vitAngD,0)

    def test_getVitesseG(self):
        self.rob.setVitAngG(4)
        self.assertEqual(self.rob.getVitesseG(), 32)
        self.rob.setVitAngG(0)
        self.assertEqual(self.rob.getVitesseG(), 0)

    def test_getVitesseD(self):
        self.rob.setVitAngD(4)
        self.assertEqual(self.rob.getVitesseD(), 32)
        self.rob.setVitAngD(0)
        self.assertEqual(self.rob.getVitesseD(), 0)

    def test_getVitesse(self):
        self.rob.changeVitAng(5)
        self.assertEqual(self.rob.getVitesse(), 40)
        self.rob.changeVitAngD(-2)
        self.assertEqual(self.rob.getVitesse(), 32)
    
    def test_capteurDistance(self):
        self.envi = Environnement(500, 300, 1)
        self.assertAlmostEqual(self.rob.capteurDistance(self.envi), 11) # Bordure de l'environnement
        self.rob.x = 50
        self.rob.y = 70
        self.rob.direction = (0, 1)
        self.rob.length = 8
        self.envi.addObstacle("test1", [(45, 94), (68, 94), (32, 159)])
        self.assertAlmostEqual(self.rob.capteurDistance(self.envi), 20) # Test pour un obstacle
        self.rob.direction = (1, 1)
        self.envi.addObstacle("test2", [(60, 71), (36, 83), (178, 178), (156, 163)]) # Test pour un autre obstacle
        self.assertAlmostEqual




    
