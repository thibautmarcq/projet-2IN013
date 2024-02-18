from Code.Interface.interface import Interface
from Code.environnement import Environnement

env = Environnement(750, 550, 1) # Initialisation de l'env
env.addObstacle('P',[(300,300),(350,300),(350,350), (300,350)])
run = Interface(env) # Lancement de l'interface
run.initRobot("Bob", 250, 250, 30, 55, 20, "lightgreen") # Initialisation du robot dans l'interface
