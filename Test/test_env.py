# python3 -m unittest Test/test_env.py -v

import unittest

from src.environnement import Environnement
from src.Robot.robot import Adaptateur_simule, Robot


class TestEnvironnement(unittest.TestCase):

    def setUp(self):
        self.env = Environnement(100, 100, 1)

    def test_init(self):
        self.assertEqual(self.env.width, 100)
        self.assertEqual(self.env.length, 100)
        self.assertEqual(self.env.listeRobots, [])
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
        rob0 = Adaptateur_simule('rob0', 10, 10, 5, 5, 2, self.env, 'lightgreen')
        rob1 = Adaptateur_simule('rob1', 20, 10, 5, 5, 2, self.env, "red")
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


    def test_addRobot(self):
        robot = Adaptateur_simule('rob1', 10, 10, 5, 5, 2, self.env, 'red')
        self.env.addRobot(robot)
        self.assertEqual(len(self.env.listeRobots), 1)
        self.assertEqual(self.env.listeRobots[0].robot.couleur, 'red')
        robot2 = Adaptateur_simule('rob2', 20, 20, 5, 5, 2, self.env, 'green')
        self.env.addRobot(robot2)
        self.assertEqual(len(self.env.listeRobots), 2)
        self.assertEqual(self.env.listeRobots[1].robot.couleur, 'green')

    def test_collision(self):
        robotA = Adaptateur_simule('rob1', self.env.width/2, self.env.length/2, 5, 5, 2, self.env, "red") # On place le robot au milieu de l'environnement
        self.env.addRobot(robotA)
        self.assertEqual(self.env.collision(robotA.robot), False)
        robotA.robot.x, robotA.robot.y = 3, self.env.length/2 # On place le robot près des murs de l'environnement pour faire une collision contre le mur
        self.assertEqual(self.env.collision(robotA.robot), True)
        robot2 = Adaptateur_simule('rob2', 10, 90, 5, 5, 2, self.env, 'green') # On place le robot au milieu de l'environnement
        self.env.addRobot(robot2)
        self.assertEqual(self.env.collision(robot2.robot), False)
        robot2.robot.x, robot2.robot.y = self.env.width/2, 3 # On place le robot près des murs de l'environnement pour faire une collision contre le mur
        self.assertEqual(self.env.collision(robot2.robot), True)
