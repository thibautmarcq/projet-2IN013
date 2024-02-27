from Code.Interface.interface import Interface
from Code.environnement import Environnement
from Code.robot import Robot
from threading import Thread
from time import sleep

def loopEnv(env):
    while True:
        env.refresh_env()
        sleep(1/60)

env = Environnement(750, 550, 1) # Initialisation de l'env
T_env = Thread(target=loopEnv, args=[env], daemon=True)
T_env.start()
env.addObstacle('J',[(400,400),(450,450),(350,450)])
env.addObstacle('P',[(300,300),(350,300),(350,350), (300,350)])
env.addObstacle('C',[(100,140),(170,55),(160,30), (130,30), (100,50), (70,30), (40,30), (30,55)])
# env.print_matrix()

# Ajoute le premier robot
robot = Robot("Bob", 250, 250, 30, 55, 20)
env.setRobot(robot, "lightgreen")

# ajoute le deuxieme robot pour test
robot2 = Robot("Stuart", 400, 250, 30, 55, 20)
env.setRobot(robot2, "red")

def menu():
    global RUNNING
    print("0 - Quit ( termine la simmu et arrete le programme )")
    print("1 - Lance une interface Graphique ")
    print("2 - afficher les infos de la simulation")
    cmd = input("Veuillez choisir une action:")
    if cmd == "0":
        RUNNING = False
    elif cmd == "1":
        run = Interface(env)
        run.mainloop()
    elif cmd == "2":
        pass



RUNNING = True

while RUNNING:
    menu()