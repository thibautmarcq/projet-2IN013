from Code.environnement import Environnement as Env
from Code.obstacle import Obstacle
from Code.robot import Robot

# Test des méthodes de la classe environnement

# Création de l'envronnement
env = Env(5, 5, 1)

# Ajout de robot et d'obstacle
env.addRobot("rob", 200, 200, 50, 50, 30)
env.addObstacle("obs")

# En fonction de la taille et en fonction de l'ordre qu'on appel addRobot et addObstacle, ils peuvent se superposer dans la matrice et peuvent se supprimer
print(env.detect_obs(env.robots[0]))

# Affichage de la matrice
print("--------------Où est le robot et l'obstacle ? ¯\_(ツ)_/¯--------------------------")

# Le chiffre 1 représente le robot et le chiffre 2 représente l'obstacle
print(env.matrice)
