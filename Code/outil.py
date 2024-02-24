import math

def normaliserVecteur(vect) :

        """ Prend en argument un vecteur et un vecteur équivalent normalisé (pour avoir une longueur de 1)
            :param vect: le vecteur que l'on souhaite normaliser
            :returns: un vecteur correspondant au vecteur donné en argument, mais normalisé à 1 de longueur
        """
        x, y = vect
        long = math.sqrt(x**2 + y**2) # la longueur du vecteur tel quel
        return (x/long, y/long) # on divise chacune des coordonnées par la longueur du vecteur, de cette manière le vecteur sera de norme 1

