from Code.Interface.newinterface import Interface
from Code.environnement import Environnement

env = Environnement(750, 550, 25) # Initialisation de l'env
run = Interface(env) # Lancement de l'interface
run.initRobot("Bob", 150, 45, 30, 55, 1, "pink") # Initialisation du robot dans l'interface
