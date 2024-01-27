import environnement as Env
import obstacle as Obstacle
import robot as Robot

# Création de l'envronnement
env = Env.Environnement(5, 5, 1)
# Ajout de robot et d'obstacle
env.addRobot("rob", 0, 0, 1, 1, 1)
env.addObstacle("obs")
# En fonction de la taille et en fonction de l'ordre qu'on appel addRobot et addObstacle, ils peuvent se superposer dans la matrice et peuvent se supprimer
print(env.detect_obs(env.robots[0]))

# Boucle pour savoir où est le robot
print("--------------Où est le robot ? ¯\_(ツ)_/¯--------------------------")
for i in range(len(env.matrice)) :
    for j in range(len(env.matrice)) :
        print("i :", i, ", j :", j)
        if ( isinstance(env.matrice[i][j], Robot.Robot) ) :
            env.matrice[i][j].afficher_etat()
        else :
            print("Ce n'est pas un robot")
# Boucle pour savoir où est l'obstacle
print("--------------Où est l'obstacle ? ¯\_(ツ)_/¯--------------------------")
for i in range(len(env.matrice)) :
    for j in range(len(env.matrice)) :
        print("i :", i, ", j :", j)
        if ( isinstance(env.matrice[i][j], Obstacle.Obstacle) ) :
            print(env.matrice[i][j].presenter_obstacle())
        else :
            print("Ce n'est pas un obstacle")