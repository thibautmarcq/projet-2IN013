import math

def normaliserVecteur(u) :

    """ Prend en argument un vecteur et un vecteur équivalent normalisé (pour avoir une longueur de 1)
        :param vect: le vecteur que l'on souhaite normaliser
        :returns: un vecteur correspondant au vecteur donné en argument, mais normalisé à 1 de longueur
    """
    x, y = u
    long = math.sqrt(x**2 + y**2) # la longueur du vecteur tel quel
    return (x/long, y/long) # on divise chacune des coordonnées par la longueur du vecteur, de cette manière le vecteur sera de norme 1

def norme(u) :
        
    """ Calcule la norme d'un vecteur
        :param u: le vecteur dont on veut calculer la norme
        :returns: la norme du vecteur passé en argument
    """

    x, y = u
    return math.sqrt(x*x + y*y)

def prodScalaire(u, v) :
        
    """ Calcule le produit scalaire de deux vecteurs
        :param u: premier vecteur qu'on utilise pour calculer le produit scalaire
        :param v: deuxième vecteur qu'on utilise pour calculer le produit scalaire
        :returns: le produit scalaire des vecteurs u et v
    """

    x1, y1 = u
    x2, y2 = v
    return x1*x2 + y1*y2

def getAngleFromVect(u, v) :

    """ Calcule l'angle entre deux vecteurs
        :param u: le premier des deux vecteurs entre lesquels on veut calculer l'angle
        :param v: le deuxième des deux vecteurs entre lesquels on veut calculer l'angle
        :returns: l'angle entre les vecteurs u et v 
    """

    # On s'assure que la valeur qu'on va donner en argument de la fonction acos est bien comprise entre -1 et 1
    cos_theta = min(1, max(-1, prodScalaire(u, v) / (norme(u) * norme(v))))
    return math.acos(cos_theta) * 180 / math.pi ## on multiplie le résultat par 180/pi pour avoir une valeur de retour en degré et non en radians

def distance(p1, p2) :
    """ Calcule la distance entre deux points p1 et p2
        :param p1: premier point 
        :param p2: deuxième point
        :returns: retourne la distance entre les deux points passés en argument
    """

    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
    