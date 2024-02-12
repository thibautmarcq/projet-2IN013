from Code.Interface.newinterface import Interface
from Code.environnement import Environnement

env = Environnement(850, 650, 25)
run = Interface(env)
run.initRobot("Bob", 150, 45, 30, 55, 1, "pink")
