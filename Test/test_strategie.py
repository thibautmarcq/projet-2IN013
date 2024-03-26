import unittest

from src.Controleur.Strategies import *
from src.environnement import Environnement
from src.Robot.robot import Adaptateur_simule


class TestControleur(unittest.TestCase):
    def setUp(self):
        self.env = Environnement(70, 55, 1)
        self.rob = Adaptateur_simule("Rob", 10, 15, 5, 7, 8, self.env)

    def test_setStrategieCarre(self):
        setStrategieCarre(self.rob, 20)
        self.assertAlmostEqual(self.rob.x, 10)
        self.assertAlmostEqual(self.rob.y, 15)

    def test_setStrategieArretMur(self):
        setStrategieArretMur(self.rob, 20)
        self.assertGreaterEqual(20,self.rob.capteurDistance())

    def test_strategieAvancer(self):
        self.strat = StrategieAvancer(self.rob, 200)
        self.strat.start()
        self.rob.x, self.rob.y = (self.rob.x+50*self.rob.direction[0], self.rob.y+50*self.rob.direction[1]) # On place le robot à une position arbitraire ( remplace le déplacement d'une distance de 50 dans la direction du robot )
        self.strat.step()
        self.assertEqual(self.strat.parcouru, 50.0)
        self.assertEqual(self.strat.stop(), False)
        self.rob.x, self.rob.y = (self.rob.x-20*self.rob.direction[0], self.rob.y-20*self.rob.direction[1]) # On place le robot à une position arbitraire ( remplace le déplacement d'une distance de 50 dans la direction du robot )
        self.strat.step()
        self.assertEqual(self.strat.parcouru, 70.0)
        self.assertEqual(self.strat.stop(), False)
        self.rob.x, self.rob.y = (self.rob.x+0*self.rob.direction[0], self.rob.y-0*self.rob.direction[1]) # On place le robot à une position arbitraire ( remplace le déplacement d'une distance de 50 dans la direction du robot )
        self.strat.step()
        self.assertEqual(self.strat.parcouru, 70.0)
        self.assertEqual(self.strat.stop(), False)
        self.rob.x, self.rob.y = (self.rob.x+130*self.rob.direction[0], self.rob.y+130*self.rob.direction[1]) # On place le robot à une position arbitraire ( remplace le déplacement d'une distance de 50 dans la direction du robot )
        self.strat.step()
        self.assertEqual(self.strat.parcouru, 200.0)
        self.assertEqual(self.strat.stop(), True)