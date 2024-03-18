# python3 -m unittest Test/test_outil.py -v
import unittest
import math
import Code.outil as outil

class TestOutil(unittest.TestCase):

    def test_normaliserVecteur(self):
        self.assertEqual(outil.normaliserVecteur((3, 4)), (0.6, 0.8))
        self.assertEqual(outil.normaliserVecteur((0, 0)), (0, 0)) # Vecteur nul
        self.assertEqual(outil.normaliserVecteur((-3, -4)), (-0.6, -0.8)) # Valeurs négatives

    def test_norme(self):
        self.assertEqual(outil.norme((3, 4)), 5.0)
        self.assertEqual(outil.norme((0, 0)), 0) # Vecteur nul
        self.assertEqual(outil.norme((-3, -4)), 5.0) # Valeurs négatives

    def test_prodScalaire(self):
        self.assertEqual(outil.prodScalaire((1, 2), (3, 4)), 11)
        self.assertEqual(outil.prodScalaire((0, 0), (3, 4)), 0) # Produit scalaire avec vecteur nul
        self.assertEqual(outil.prodScalaire((-1, -2), (-3, -4)), 11) # Valeurs négatives

    def test_getAngleFromVect(self):
        self.assertAlmostEqual(outil.getAngleFromVect((1, 0), (0, 1)), 90.0)
        self.assertAlmostEqual(outil.getAngleFromVect((1, 0), (1, 0)), 0.0) # Angle entre le même vecteur
        self.assertAlmostEqual(outil.getAngleFromVect((-1, 0), (0, -1)), 90.0) # Valeurs négatives, vecteurs orthogonaux

    def test_distance(self):
        self.assertEqual(outil.distance((1, 2), (4, 6)), 5.0)
        self.assertEqual(outil.distance((1, 2), (1, 2)), 0.0) # Distance entre les 2 memes points 
        self.assertEqual(outil.distance((-1, -2), (-4, -6)), 5.0) # Valeurs négatives

    def test_getVectFromAngle(self):

        vect = [1, 0]
        newv = outil.getVectFromAngle(vect, 45)
        xp, yp = newv
        self.assertAlmostEqual(xp, math.sqrt(2)/2)
        self.assertAlmostEqual(yp, math.sqrt(2)/2)

        vect = [2, -4]
        newv = outil.getVectFromAngle(vect, 90)
        xp, yp = newv
        self.assertAlmostEqual(xp, 4)
        self.assertAlmostEqual(yp, 2)

        vect = [3, 4]
        newv = outil.getVectFromAngle(vect, -30)
        xp, yp = newv
        self.assertLess(abs(xp-4.598), 0.01)
        self.assertLess(abs(yp-1.964), 0.01)
        