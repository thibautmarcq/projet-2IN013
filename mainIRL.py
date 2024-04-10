# Main à lancer sur le robot pour exécuter des stratégies/actions

from logging import DEBUG, basicConfig

from robot2IN013 import Robot2IN013
from src.controleurs import Controler, setStrategieArretMur, setStrategieCarre
from src.robots import Adaptateur_reel

basicConfig(filename='logs.log', 
                    level=DEBUG, 
                    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', 
                    datefmt='%d/%m/%y %H:%M:%S', 
                    encoding='UTF-8') # niveaux : DEBUG INFO WARNING ERROR CRITICAL

#On crée un controleur
controleur = Controler()

# Crée le premier robot
robreel = Robot2IN013()

# Adapte le robot
reel = Adaptateur_reel(robreel)

def menu() :
    """
    Fonction qui affiche un menu pour choisir une action
    """
    global RUNNING
    print("0 - Quitter")
    print("1 - Tracer un carré")
    print("2 - Avancer vers le mur sans se crasher")
    print("3 - Stratégie séquentielle")
    cmd = int(input("Veuillez choisir une action :\n"))
    if cmd==0:
        RUNNING = False
    elif cmd== 1:
        long = float(input("Quelle largeur voulez-vous pour le carré ? \n"))
        carre = setStrategieCarre(reel, long)
        controleur.lancerStrategie(carre)
    elif cmd==2:
        long = float(input("A quelle distance doit-on s'arrêter du mur ?"))
        mur = setStrategieArretMur(reel, long)
        controleur.lancerStrategie(mur)
    elif cmd==3:
        pass
    else:
        print("Numéro non disponible")

RUNNING = True
while RUNNING:
    menu()