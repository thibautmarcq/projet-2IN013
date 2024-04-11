from src.interface2D import menu2D

RUNNING = True

while RUNNING:
    print("0 - Quit (termine la simulation et arrête le programme)")
    print("1 - Lance une interface Graphique ")
    print("2 - Afficher les infos de la simulation")
    print("3 - Faire tracer un carré au robot réel")

    cmd = input("Veuillez choisir une action:\n")
    if cmd == "0":
        RUNNING = False
    else:
        menu2D(cmd)