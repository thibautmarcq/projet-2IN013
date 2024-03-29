import unittest

from src.environnement import Environnement
from src.outil import distance
from src.Robot.robot import Adaptateur_simule


class TestAdaptateurSimu(unittest.TestCase):
    def setUp(self) :
        self.env = Environnement(500,300,1)
        self.rob = Adaptateur_simule("Rob", 10, 15, 5, 7, 8, self.env)
    
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
        self.assertEqual(self.rob.estCrash, False)
        self.assertEqual(self.rob.estSousControle, False)
        self.assertEqual(self.rob.last_point, (self.rob.x, self.rob.y))
        self.assertEqual(self.rob.last_dir, self.rob.direction)
        self.assertEqual(self.rob.env, self.env)

    def test_setVitAngG(self):
        self.rob.setVitAngGA(5)
        self.assertEqual(self.rob.vitAngG,5)
        self.rob.setVitAngGA(-7)
        self.assertEqual(self.rob.vitAngG,-7)
        self.rob.setVitAngGA(0)
        self.assertEqual(self.rob.vitAngG,0)

    def test_setVitAngD(self):
        self.rob.setVitAngDA(5)
        self.assertEqual(self.rob.vitAngD,5)
        self.rob.setVitAngDA(-7)
        self.assertEqual(self.rob.vitAngD,-7)
        self.rob.setVitAngDA(0)
        self.assertEqual(self.rob.vitAngD,0)

    def test_setVitAng(self):
        self.rob.setVitAngA(5)
        self.assertEqual((self.rob.vitAngD, self.rob.vitAngG),(5,5))
        self.rob.setVitAngA(-7)
        self.assertEqual((self.rob.vitAngD, self.rob.vitAngG),(-7,-7))
        self.rob.setVitAngA(0)
        self.assertEqual((self.rob.vitAngD, self.rob.vitAngG),(0,0))

    def test_capteurDistance(self):
        self.assertAlmostEqual(self.rob.capteurDistanceA(), 11) # Bordure de l'environnement
        self.rob.x = 50
        self.rob.y = 70
        self.rob.direction = (0, 1)
        self.rob.length = 8
        self.env.addObstacle("test1", [(45, 94), (68, 94), (32, 159)])
        self.assertAlmostEqual(self.rob.capteurDistanceA(), 20) # Test pour un obstacle
        self.rob.direction = (1, 1)
        self.env.addObstacle("test2", [(60, 71), (36, 83), (178, 178), (156, 163)]) # Test pour un autre obstacle
        self.assertAlmostEqual(self.rob.capteurDistanceA(), 0) # Test pour un autre obstacle

    def test_distanceParcourue(self):
        self.rob.x, self.rob.y = 0, 0
        self.assertAlmostEqual(self.rob.distance_parcourue(), 18.0, places=1)
        self.rob.x = 67
        self.assertEqual(self.rob.distance_parcourue(), 67.0)
        self.rob.y = 10
        self.assertEqual(self.rob.distance_parcourue(), 10.0)
        self.rob.x = -300
        self.assertEqual(self.rob.distance_parcourue(), 367.0)
        self.rob.y = -123
        self.assertEqual(self.rob.distance_parcourue(), 133.0)
        self.rob.x, self.rob.y = (-100, 2)
        self.assertAlmostEqual(self.rob.distance_parcourue(), 235.8, places=1)
        self.rob.x, self.rob.y = (241, -231)
        self.assertAlmostEqual(self.rob.distance_parcourue(), 413.0, places=1)
        self.rob.x, self.rob.y = (-100, -231)
        self.assertEqual(self.rob.distance_parcourue(), 341.0)

    def test_angleParcourue(self):
        self.rob.direction = (0, 1)
        self.assertEqual(self.rob.angle_parcouru(), 180.0)
        self.rob.direction = (1, 1)
        self.assertAlmostEqual(self.rob.angle_parcouru(), 45.0)
        self.rob.direction = (-1, -1)
        self.assertAlmostEqual(self.rob.angle_parcouru(), 180.0, places=1)
        self.rob.direction = (1, -1)
        self.assertEqual(self.rob.angle_parcouru(), 90.0)
        self.rob.direction = (-1, 1)
        self.assertAlmostEqual(self.rob.angle_parcouru(), 180.0, places=1)
        self.rob.direction = (0.5, 1)
        self.assertAlmostEqual(self.rob.angle_parcouru(), 71.6, places=1)
        self.rob.direction = (0.1, -0.4)
        self.assertAlmostEqual(self.rob.angle_parcouru(), 139.4, places=1)