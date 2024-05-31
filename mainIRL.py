# Main à lancer sur le robot pour exécuter des stratégies/actions

from logging import DEBUG, basicConfig
import curses

from robot2IN013 import Robot2IN013
from src import Controler, setStrategieArretMur, setStrategieCarre, StrategieSuivreBalise, StrategieRobocar, Adaptateur_reel, play_audio_with_volume

basicConfig(filename='logs.log', 
                    level=DEBUG, 
                    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', 
                    datefmt='%d/%m/%y %H:%M:%S', 
                    encoding='UTF-8') # niveaux : DEBUG INFO WARNING ERROR CRITICAL
#On crée un controleur
controleur = Controler()

# Crée le premier robot
robreel = Robot2IN013()
robreel.start_recording()

# Adapte le robot
reel = Adaptateur_reel(robreel)
reel.vitAngD = 0
reel.vitAngG = 0
reel.sonNow = None

def menu() :
    """ Fonction qui affiche un menu pour choisir une action """
    global RUNNING
    print("0 - Quitter")
    print("1 - Tracer un carré")
    print("2 - Avancer vers le mur sans se crasher")
    print("3 - Avancer avec les touches du clavier")
    print("4 - Suivre balise")
    print("5 - Robocar")
    cmd = int(input("Veuillez choisir une action :\n"))
    if cmd==0:
        RUNNING = False
        robreel.stop_recording()
    elif cmd== 1:
        long = float(input("Quelle largeur voulez-vous pour le carré ? \n"))
        carre = setStrategieCarre(reel, long)
        controleur.lancerStrategie(carre)
    elif cmd==2:
        long = float(input("A quelle distance doit-on s'arrêter du mur ?"))
        mur = setStrategieArretMur(reel, long)
        controleur.lancerStrategie(mur)
    elif cmd==3: # Contrôle manuel
        CMD = True
        def display_message(stdscr, message):
            stdscr.addstr(3, 0, message)
            stdscr.clrtoeol()
            stdscr.refresh()

        def get_key(stdscr):
            stdscr.nodelay(1)
            stdscr.timeout(100) # évite les appuis longs
            while True and CMD:
                key = stdscr.getch()
                if key != -1:
                    return key
                curses.napms(50) 
        stdscr = curses.initscr()

        curses.curs_set(0)  # pas de curseur
        stdscr.clear()
        stdscr.addstr(0, 0, "Contrôles du robot :\n a z e \n q s d")
        stdscr.refresh()
        while True and CMD:
            key = get_key(stdscr)
            
            if key != -1:
                display_message(stdscr, f"Touche {chr(key)}\n")

                if key == ord('a'):
                    reel.vitAngG+=0.5
                    reel.setVitAngGA(reel.vitAngG)
                    display_message(stdscr, "+RG")
                elif key == ord('z'):
                    reel.vitAngG+=0.5
                    reel.setVitAngGA(reel.vitAngG)
                    reel.vitAngD+=0.5
                    reel.setVitAngDA(reel.vitAngD)
                    display_message(stdscr, "+Global")
                elif key == ord('e'):
                    reel.vitAngD+=0.5
                    reel.setVitAngDA(reel.vitAngD)
                    display_message(stdscr, "+RD")
                elif key == ord('q'):
                    reel.vitAngG-=0.5
                    reel.setVitAngGA(reel.vitAngG)
                    display_message(stdscr, "-RG")
                elif key == ord('s'):
                    reel.vitAngG-=0.5
                    reel.setVitAngGA(reel.vitAngG)
                    reel.vitAngD-=0.5
                    reel.setVitAngDA(reel.vitAngD)
                    display_message(stdscr, "-Global")              
                elif key == ord('d'):
                    reel.vitAngD-=0.5
                    reel.setVitAngDA(reel.vitAngD)
                    display_message(stdscr, "-RD")
                elif key == ord('p'):
                    CMD = False
                    curses.endwin()
                    print('prout')
                    reel.setVitAngA(0)
                    robreel.stop_recording()
                    
                    
    elif cmd==4:
        balise = StrategieSuivreBalise(reel)
        controleur.lancerStrategie(balise)

    elif cmd==5:
        robocar = StrategieRobocar(reel)
        controleur.lancerStrategie(robocar)
  
    else:
        print("Numéro non disponible")

RUNNING = True
while RUNNING:
    menu()

