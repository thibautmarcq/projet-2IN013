# python3 -m unittest Test/test_env.py -v

import unittest
from Code.environnement import Environnement
from Code.robot import Robot

class TestEnvironnement(unittest.TestCase):

    def setUp(self):
        self.env = Environnement(100, 100, 1)

    def test_init(self):
        self.assertEqual(self.env.width, 100)
        self.assertEqual(self.env.length, 100)
        self.assertEqual(self.env.robots, [])
        self.assertEqual(self.env.robotSelect, 0)
        self.assertEqual(self.env.scale, 1)
        self.assertEqual(self.env.last_refresh, 0)
        self.assertEqual(self.env.listeObs, [])

    def test_initMatrice(self):
        self.env.initMatrice()
        self.assertEqual(self.env.matrice[0][0], 2) # angle
        self.assertEqual(self.env.matrice[-1][0], 2)
        self.assertEqual(self.env.matrice[-1][5], 2)
        self.assertEqual(self.env.matrice[0][5], 2)

    def test_addRobotSelect(self):
        self.env.addRobotSelect(1) # test d'ajout alors que pas de robot
        self.assertEqual(self.env.robotSelect, 0) 
        rob0 = Robot('rob0', 10, 10, 5, 5, 2)
        rob1 = Robot('rob1', 20, 10, 5, 5, 2)
        self.env.addRobot(rob0)
        self.env.addRobotSelect(1) # test avec robot
        self.assertEqual(self.env.robotSelect, 0)
        self.env.addRobot(rob1)
        self.env.addRobotSelect(1) # test avec robot
        self.assertEqual(self.env.robotSelect, 1) 

    def test_addObstacle(self):
        self.env.addObstacle('obs1', [(10, 10), (20, 20)]) # ligne (basique)
        self.assertEqual(len(self.env.listeObs), 1) # 1 obs dans la liste
        self.assertEqual(self.env.matrice[10][10], 2) # point défini
        self.assertEqual(self.env.matrice[15][15], 2) # point au milieu


    def test_setRobot(self):
        robot = Robot('rob1', 10, 10, 5, 5, 2)
        self.env.setRobot(robot, 'red')
        self.assertEqual(len(self.env.robots), 1)
        self.assertEqual(self.env.robots[0].couleur, 'red')

    def test_addRobot(self):
        robot = Robot('rob3', 10, 10, 5, 5, 2)
        self.env.addRobot(robot)
        self.assertEqual(len(self.env.robots), 1)
        self.assertEqual(self.env.matrice[10][10], 1) # robot représenté par un 1


