from srcMainALL import menu

RUNNING = True

while RUNNING:
    print("0 - Quit (termine la simulation et arrête le programme)")
    print("1 - Lance une interface 2D ")
    print("2 - Lance une interface 3D")
    print("3 - afficher les infos de la simulation")

    cmd = input("Veuillez choisir une action:\n")
    if cmd == "0":
        RUNNING = False
    else:
        menu(cmd)