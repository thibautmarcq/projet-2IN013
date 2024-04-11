# python3 -m unittest Test/test_py -v
from math import sqrt
from unittest import TestCase

from src import (getAngleFromVect, getDistanceFromPts, getVectFromAngle,
                 normaliserVecteur, norme, prodScalaire)


class TestOutil(TestCase):

    def test_normaliserVecteur(self):
        self.assertEqual(normaliserVecteur((3, 4)), (0.6, 0.8))
        self.assertEqual(normaliserVecteur((0, 0)), (0, 0)) # Vecteur nul
        self.assertEqual(normaliserVecteur((-3, -4)), (-0.6, -0.8)) # Valeurs négatives

    def test_norme(self):
        self.assertEqual(norme((3, 4)), 5.0)
        self.assertEqual(norme((0, 0)), 0) # Vecteur nul
        self.assertEqual(norme((-3, -4)), 5.0) # Valeurs négatives

    def test_prodScalaire(self):
        self.assertEqual(prodScalaire((1, 2), (3, 4)), 11)
        self.assertEqual(prodScalaire((0, 0), (3, 4)), 0) # Produit scalaire avec vecteur nul
        self.assertEqual(prodScalaire((-1, -2), (-3, -4)), 11) # Valeurs négatives

    def test_getAngleFromVect(self):
        self.assertAlmostEqual(getAngleFromVect((1, 0), (0, 1)), 90.0)
        self.assertAlmostEqual(getAngleFromVect((1, 0), (1, 0)), 0.0) # Angle entre le même vecteur
        self.assertAlmostEqual(getAngleFromVect((-1, 0), (0, -1)), 90.0) # Valeurs négatives, vecteurs orthogonaux

    def test_getDistanceFromPts(self):
        self.assertEqual(getDistanceFromPts((1, 2), (4, 6)), 5.0)
        self.assertEqual(getDistanceFromPts((1, 2), (1, 2)), 0.0) # Distance entre les 2 memes points 
        self.assertEqual(getDistanceFromPts((-1, -2), (-4, -6)), 5.0) # Valeurs négatives

    def test_getVectFromAngle(self):

        vect = [1, 0]
        newv = getVectFromAngle(vect, 45)
        xp, yp = newv
        self.assertAlmostEqual(xp, sqrt(2)/2)
        self.assertAlmostEqual(yp, sqrt(2)/2)

        vect = [2, -4]
        newv = getVectFromAngle(vect, 90)
        xp, yp = newv
        self.assertAlmostEqual(xp, 4)
        self.assertAlmostEqual(yp, 2)

        vect = [3, 4]
        newv = getVectFromAngle(vect, -30)
        xp, yp = newv
        self.assertLess(abs(xp-4.598), 0.01)
        self.assertLess(abs(yp-1.964), 0.01)
        