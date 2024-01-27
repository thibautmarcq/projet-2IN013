import environnement as Env
import obstacle as Obstacle
import robot as Robot

env = Env.Environnement(25, 25, 5)
env.addRobot("rob", 0, 0,1,1,1)
env.addObstacle("obs", )
print(env.detect_obs(env.robots[0]))
for i in range(len(env.matrice)) :
    for j in range(len(env.matrice)) :
        print("i :", i, ", j :", j)
        if ( isinstance(env.matrice[i][j], Robot.Robot) ) :
            print(env.matrice[i][j].afficher_etat())
        else :
            print("Ce n'est pas un robot")