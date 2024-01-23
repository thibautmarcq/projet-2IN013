class Obstacle :

    def __init__(nom, posx, posy) :
        self.nom = nom
        self.x = posx
        self.y = posy


class Robot :
    def __init__(self, position_x, position_y, obstacles):
        self.posx = position_x
        self.posy = position_y
        self.obstacles = obstacles
    
    def avancer(self, quantite) :
        trouve = False
        for o in self.obstacles :
            if o.y == self.posx and (self.posy+quantite)==o.y :
                trouve = True
                print("Je ne peux pas avancer en (" + self.posx + ", " + (self.posy + quantite) + ") car il y a l'obstacle " + o.nom)
                return
            
        if trouve == False :
            printf("Position précédente : (" + self.posx + ", " + self.posy + "), nouvelle position : (" + self.posx + ", " + (self.posy + quantite) + ")" )
            self.posy = self.posy + quantite


    def reculer(self, quantite) :
        if self.posy-quantite < 0 :
            print("Le déplacement n'est pas possible car hors champ")
            return
        trouve = False
        for o in self.obstacles :
            if o.y == self.posx and (self.posy-quantite)==o.y :
                trouve = True
                print("Je ne peux pas avancer en (" + self.posx + ", " + (self.posy - quantite) + ") car il y a l'obstacle" + o.nom)
                return
            
        if trouve == False :
            printf("Position précédente : (" + self.posx + ", " + self.posy + "), nouvelle position : (" + self.posx + ", " + (self.posy - quantite) + ")")
            self.posy = self.posy - quantite

    def droite(self, quantite) :
        trouve = False
        for o in self.osbtacles :
            if o.x == self.posx and (self.posx + quantite) == o.x :
                trouve = True
                print("Je ne peux pas avancer en (" + (self.posx + quantite) + ", " + self.posy + ") car il y a l'obstacle" + o.nom)
                return
        
        if trouve == False :
            printf("Position précédente : (" + self.posx + ", " + self.posy + "), nouvelle position : (" + (self.posx + quantite) + ", " + self.posy + ")")
            self.posx = self.posxy + quantite

    def gauche(self, quantite) :
        if self.posx-quantite < 0 :
            print("Le déplacement n'est pas possible car hors champ")
            return
        trouve = False
        for o in self.osbtacles :
            if o.x == self.posx and (self.posx - quantite) == o.x :
                trouve = True
                print("Je ne peux pas avancer en (" + (self.posx - quantite) + ", " + self.posy + ") car il y a l'obstacle" + o.nom)
                return
        
        if trouve == False :
            printf("Position précédente : (" + self.posx + ", " + self.posy + "), nouvelle position : (" + (self.posx - quantite) + ", " + self.posy + ")")
            self.posx = self.posxy - quantite

    def get_position(self) :
        return (self.posx, self.posy)  
    
    def afficher_etat(self) :
        print("Je suis le robot " + self.nom + " et je suis à la position" + self.get_position)

    def deplacement(self) :
        boucle = True
        while boucle :
            print("----------------------------------")
            print("Choisir une option : a pour avancer, r pour reculer, d pour aller a droite, g pour aller a gauche, ou q pour quitter")
            depl = input()
            quantite = 0
            if depl in ['a', 'r', 'd', 'g'] :
                print("Tapez de combien vous voulez vous déplacer")
                quantite = input()
            if depl == 'a' :
                self.avancer(quantite)
            elif depl == 'r' :
                self.reculer(quantite)
            elif depl == 'd' :
                self.droite(quantite)
            elif depl == 'g' :
                self.gauche(quantite)
            elif delp == 'q' :
                boucle = False
            print("Le déplacement du robot est terminé")


