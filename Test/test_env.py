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
        rob0 = Adaptateur_simule('rob0', 10, 10, 5, 5, 2, self.env)
        rob1 = Robot('rob1', 20, 10, 5, 5, 2)
        self.env.addRobot(rob0, 'lightgreen')
        self.env.addRobotSelect(1) # test avec robot
        self.assertEqual(self.env.robotSelect, 0)
        self.env.addRobot(rob1, "red")
        self.env.addRobotSelect(1) # test avec robot
        self.assertEqual(self.env.robotSelect, 1) 

    def test_addObstacle(self):
        self.env.addObstacle('obs1', [(10, 10), (20, 20)]) # ligne (basique)
        self.assertEqual(len(self.env.listeObs), 1) # 1 obs dans la liste
        self.assertEqual(self.env.matrice[10][10], 2) # point défini
        self.assertEqual(self.env.matrice[15][15], 2) # point au milieu


    def test_addRobot(self):
        robot = Adaptateur_simule('rob1', 10, 10, 5, 5, 2, self.env)
        self.env.addRobot(robot, 'red')
        self.assertEqual(len(self.env.robots), 1)
        self.assertEqual(self.env.robots[0].couleur, 'red')
        robot2 = Robot('rob2', 20, 20, 5, 5, 2)
        self.env.addRobot(robot2, 'green')
        self.assertEqual(len(self.env.robots), 2)
        self.assertEqual(self.env.robots[1].couleur, 'green')

    def test_collision(self):
        robot = Adaptateur_simule('rob1', self.env.width/2, self.env.length/2, 5, 5, 2, self.env) # On place le robot au milieu de l'environnement
        self.env.addRobot(robot, 'red')
        self.assertEqual(self.env.collision(robot), False)
        robot.x, robot.y = 3, self.env.length/2 # On place le robot près des murs de l'environnement pour faire une collision contre le mur
        self.assertEqual(self.env.collision(robot), True)
        robot2 = Robot('rob2', 10, 90, 5, 5, 2) # On place le robot au milieu de l'environnement
        self.env.addRobot(robot2, 'green')
        self.assertEqual(self.env.collision(robot2), False)
        robot2.x, robot2.y = self.env.width/2, 3 # On place le robot près des murs de l'environnement pour faire une collision contre le mur
        self.assertEqual(self.env.collision(robot2), True)
