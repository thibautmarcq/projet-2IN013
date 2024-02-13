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
        self.assertEqual(self.rob.nbToursRoueD, 0)
        self.assertEqual(self.rob.nbToursRoueG, 0)

    def test_setVitesse(self):
        self.rob.setVitesse(12)
        self.assertEqual(self.rob.vitesse, 12)

    def test_rotation(self):
        self.rob.rotation()
        dirx,diry = self.rob.direction
        self.assertAlmostEqual(dirx, 0)
        self.assertAlmostEqual(diry, -1)

    def test_avancer(self):
        self.rob.avancerDirection(10)
        self.assertEqual(self.rob.x, 10)
        self.assertEqual(self.rob.y, 5)

    def test_reculer(self):
        self.rob.setVitesse(8)
        self.rob.reculerDirection()
        self.assertEqual(self.rob.x, 10)
        self.assertEqual(self.rob.y, 23)

    def test_vitesses_roues(self) :
        self.rob.setTourG(9.8)
        self.rob.setTourD(4.8)
        self.assertEqual(self.rob.nbToursRoueG, 9.8)
        self.assertEqual(self.rob.nbToursRoueD, 4.8)

        self.rob.addTourG()
        self.assertAlmostEqual(self.rob.nbToursRoueG, 9.9)
        self.rob.addTourD()
        self.assertAlmostEqual(self.rob.nbToursRoueD, 4.9)

        self.rob.addTour()
        self.assertAlmostEqual(self.rob.nbToursRoueG, 10)
        self.assertAlmostEqual(self.rob.nbToursRoueD, 5)

        vitG = self.rob.getVitesseRoueG()
        vitD = self.rob.getVitesseRoueD()
        self.assertLess(abs(vitG - 502.65), 0.01)
        self.assertLess(abs(vitD - 251.33), 0.01)

    def test_normalisation(self) :
        self.rob.direction = (13, 8)
        norme = math.sqrt(self.rob.direction[0]**2 + self.rob.direction[1]**2)
        self.assertNotAlmostEqual(1, norme)
        
        self.rob.direction = self.rob.normaliserVecteur(self.rob.direction)
        norme = math.sqrt(self.rob.direction[0]**2 + self.rob.direction[1]**2)
        self.assertAlmostEqual(norme, 1)

    def test_refresh(self) :
        self.rob.rayonRoue = 1
        self.rob.direction = (3, 4)
        self.rob.setTourD(10)
        self.rob.setTourG(10)
        x = self.rob.x
        y = self.rob.y
        self.rob.refresh(1)

        self.assertAlmostEqual(self.rob.vitesse, 20*math.pi)
        self.assertAlmostEqual(self.rob.direction, (3/5, 4/5))
        self.assertAlmostEqual(self.rob.x, x + 12*math.pi)
        self.assertAlmostEqual(self.rob.y, y + 16*math.pi)



    
