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


