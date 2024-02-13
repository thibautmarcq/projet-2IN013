from Code.Interface.newinterface import Interface
from Code.environnement import Environnement

env = Environnement(750, 550, 25) # Initialisation de l'env
run = Interface(env) # Lancement de l'interface
run.initRobot("Bob", 250, 250, 30, 55, 10, "pink") # Initialisation du robot dans l'interface
