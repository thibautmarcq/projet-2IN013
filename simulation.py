from Code.Interface.interface import Interface
from Code.environnement import Environnement
from Code.robot import Robot

env = Environnement(750, 550, 10) # Initialisation de l'env
env.addObstacle('J',[(400,400),(450,450),(350,450)])
env.addObstacle('P',[(300,300),(350,300),(350,350), (300,350)])
env.print_matrix()
run = Interface(env) # Lancement de l'interface
robot = Robot("Bob", 250, 250, 30, 55, 20)
env.setRobot(robot, "lightgreen")
run.mainloop() # Initialisation du robot dans l'interface