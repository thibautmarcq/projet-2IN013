import environnement as Env
import obstacle as Obstacle
import robot as Robot

# Test des méthodes de la classe environnement

# Création de l'envronnement
env = Env.Environnement(5, 5, 1)
# Ajout de robot et d'obstacle
env.addRobot("rob", 0, 0, 1, 1, 1)
env.addObstacle("obs")
# En fonction de la taille et en fonction de l'ordre qu'on appel addRobot et addObstacle, ils peuvent se superposer dans la matrice et peuvent se supprimer
print(env.detect_obs(env.robots[0]))

# Affichage ASCII pour savoir où sont placés le robot et l'obstacle
print("--------------Où est le robot et l'obstacle ? ¯\_(ツ)_/¯--------------------------")
n=0
print("|", end="")
print("M", end="")
for i in range(len(env.matrice)) :
    print("|", end="")
    print(n, end="")
    n+=1
print("|")
x=0
for i in range(len(env.matrice)) :
    print("|", end="")
    print(x,end="")
    for j in range(len(env.matrice)) :
        print("|", end="")
        if ( isinstance(env.matrice[i][j], Obstacle.Obstacle) ) :
            print("o", end="")
        elif ( isinstance(env.matrice[i][j], Robot.Robot) ) :
            print("r", end="")
        else:
            print("x", end="")
    print("|")
    x+=1
