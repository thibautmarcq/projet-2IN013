from unittest import TestCase

from src import Environnement
from src.controleur import (StrategieArretMur, StrategieAvancer,
                            StrategieTourner, distSup, setStrategieArretMur,
                            setStrategieCarre)
from src.robots import Adaptateur_simule


class TestControleur(TestCase):
    def setUp(self):
        self.env = Environnement(100, 100, 1)
        self.rob = Adaptateur_simule("Rob", 10, 15, 5, 7, 15, 8, self.env, "red")

    def test_setStrategieCarre(self):
        setStrategieCarre(self.rob, 20)
        self.assertAlmostEqual(self.rob.robot.x, 10)
        self.assertAlmostEqual(self.rob.robot.y, 15)
        self.assertAlmostEqual(self.rob.robot.x, 10)
        self.assertAlmostEqual(self.rob.robot.y, 15)

    def test_setStrategieArretMur(self):
        setStrategieArretMur(self.rob, 20)
        self.assertGreaterEqual(20,self.rob.capteurDistanceA())

    def test_strategieAvancer(self):
        self.strat = StrategieAvancer(self.rob, 200)
        self.strat.start()
        self.rob.robot.x, self.rob.robot.y = (self.rob.robot.x+50*self.rob.robot.direction[0], self.rob.robot.y+50*self.rob.robot.direction[1]) # On place le robot à une position arbitraire ( remplace le déplacement d'une distance de 50 dans la direction du robot )
        self.rob.robot.x, self.rob.robot.y = (self.rob.robot.x+50*self.rob.robot.direction[0], self.rob.robot.y+50*self.rob.robot.direction[1]) # On place le robot à une position arbitraire ( remplace le déplacement d'une distance de 50 dans la direction du robot )
        self.strat.step()
        self.assertEqual(self.strat.parcouru, 50.0)
        self.assertEqual(self.strat.stop(), False)
        self.rob.robot.x, self.rob.robot.y = (self.rob.robot.x-20*self.rob.robot.direction[0], self.rob.robot.y-20*self.rob.robot.direction[1]) 
        self.rob.robot.x, self.rob.robot.y = (self.rob.robot.x-20*self.rob.robot.direction[0], self.rob.robot.y-20*self.rob.robot.direction[1]) 
        self.strat.step()
        self.assertEqual(self.strat.parcouru, 70.0)
        self.assertEqual(self.strat.stop(), False)
        self.rob.robot.x, self.rob.robot.y = (self.rob.robot.x+0*self.rob.robot.direction[0], self.rob.robot.y-0*self.rob.robot.direction[1]) 
        self.rob.robot.x, self.rob.robot.y = (self.rob.robot.x+0*self.rob.robot.direction[0], self.rob.robot.y-0*self.rob.robot.direction[1]) 
        self.strat.step()
        self.assertEqual(self.strat.parcouru, 70.0)
        self.assertEqual(self.strat.stop(), False)
        self.rob.robot.x, self.rob.robot.y = (self.rob.robot.x+130*self.rob.robot.direction[0], self.rob.robot.y+130*self.rob.robot.direction[1]) 
        self.rob.robot.x, self.rob.robot.y = (self.rob.robot.x+130*self.rob.robot.direction[0], self.rob.robot.y+130*self.rob.robot.direction[1]) 
        self.strat.step()
        self.assertEqual(self.strat.parcouru, 200.0)
        self.assertEqual(self.strat.stop(), True)

    def test_strategieTourner(self):
        self.strat = StrategieTourner(self.rob, 90)
        self.strat.start()
        self.rob.robot.direction = (1, -1)
        self.rob.robot.direction = (1, -1)
        self.strat.step()
        self.assertAlmostEqual(self.strat.angle_parcouru, 45.0)
        self.assertEqual(self.strat.stop(), False)
        self.rob.robot.direction = (1, 0)
        self.rob.robot.direction = (1, 0)
        self.strat.step()
        self.assertAlmostEqual(self.strat.angle_parcouru, 90.0)
        self.assertEqual(self.strat.stop(), True)
        
        self.rob.robot.direction = (0, -1)
        self.rob.robot.direction = (0, -1)
        self.strat.angle_parcouru = 0
        self.strat = StrategieTourner(self.rob, -90)
        self.strat.start()
        self.rob.robot.direction = (-1,-1)
        self.rob.robot.direction = (-1,-1)
        self.strat.step()
        self.assertAlmostEqual(self.strat.angle_parcouru, 45.0)
        self.assertEqual(self.strat.stop(), False)
        self.rob.robot.direction = (0,-1)
        self.rob.robot.direction = (0,-1)
        self.strat.step()
        self.assertAlmostEqual(self.strat.angle_parcouru, 90.0)
        self.assertEqual(self.strat.stop(), True)
    
    def test_strategieArretMur(self):
        self.strat = StrategieArretMur(self.rob, 10)
        self.rob.robot.x, self.rob.robot.y = self.env.width/2, self.env.length/2
        self.rob.robot.x, self.rob.robot.y = self.env.width/2, self.env.length/2
        self.strat.start()
        self.assertEqual(self.strat.distrob, 46)
        self.assertEqual(self.strat.stop(), False)
        self.rob.robot.x, self.rob.robot.y = (self.rob.robot.x+0*self.rob.robot.direction[0], self.rob.robot.y+10*self.rob.robot.direction[1]) # On place le robot à une position arbitraire ( remplace le déplacement d'une distance de 10 dans la direction du robot )
        self.rob.robot.x, self.rob.robot.y = (self.rob.robot.x+0*self.rob.robot.direction[0], self.rob.robot.y+10*self.rob.robot.direction[1]) # On place le robot à une position arbitraire ( remplace le déplacement d'une distance de 10 dans la direction du robot )
        self.strat.step()
        self.assertEqual(self.strat.distrob, 36)
        self.assertEqual(self.strat.stop(), False)
        self.rob.robot.x, self.rob.robot.y = (self.rob.robot.x+0*self.rob.robot.direction[0], self.rob.robot.y+30*self.rob.robot.direction[1])
        self.rob.robot.x, self.rob.robot.y = (self.rob.robot.x+0*self.rob.robot.direction[0], self.rob.robot.y+30*self.rob.robot.direction[1])
        self.strat.step()
        self.assertEqual(self.strat.distrob, 6)
        self.assertEqual(self.strat.stop(), True)

    def test_distSup(self):
        self.assertEqual(distSup(self.rob, 10), True)
