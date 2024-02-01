import unittest

from Code import obstacle 

class TestObstacle(unittest.TestCase):
    def setUp(self) :
        self.obs = obstacle("Pierre", 20, 30)

    def test_coords(self):
        self.assertEqual(self.obs.x, 20)
        self.assertEqual(self.obs.y, 30)
        self.assertEqual(self.obs.nom, "Pierre" )

    if __name__ == '__main__':
        unittest.main()