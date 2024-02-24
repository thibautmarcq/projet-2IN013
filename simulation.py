from Code.Interface.interface import Interface
from Code.environnement import Environnement
from Code.robot import Robot

env = Environnement(750, 550, 6) # Initialisation de l'env
env.addObstacle('J',[(400,400),(450,450),(350,450)])
env.addObstacle('P',[(300,300),(350,300),(350,350), (300,350)])
env.addObstacle('C',[(100,140),(170,55),(160,30), (130,30), (100,50), (70,30), (40,30), (30,55)])
env.print_matrix()
run = Interface(env) # Lancement de l'interface
robot = Robot("Bob", 250, 250, 30, 55, 20)
env.setRobot(robot, "lightgreen")

#ajout d'un deuxieme robot pour test
robot2 = Robot("Stuart", 400, 250, 30, 55, 20)
env.setRobot(robot2, "red")
run.mainloop() # Initialisation du robot dans l'interface