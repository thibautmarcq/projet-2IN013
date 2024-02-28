from Code.outil import *
import time

REFRESH_DT = 1/30

class StrategieAvancer:
    
    def __init__(self, rob, distance) :
        """ Statégie qui fait avancer le robot d'une distance donnée
            :param distance: la distance que doit parcourir le robot  
            :param rob: le robot qui va avancer
            :param parcouru: la distance parcourue du robot
            :returns: ne retourne rien, on initialise la stratégie
        """
        self.distance = distance
        self.rob = rob 
        self.parcouru = 0
        self.pt_depart = (self.rob.x, self.rob.y)
  
    def start(self) :
        self.rob.estSousControle = True
        self.parcouru = 0
        self.pt_depart = (self.rob.x, self.rob.y)
        self.rob.setVitAng(0) # On initialise les vitesses angulaires des deux roues à 0
        self.rob.changeVitAng(1) # Puis on augmente les vitesses angulaires de 0.01
        self.step()

    def step(self) : 
        """ On fait avancer le robot d'un petit pas
            :returns: rien, on met juste à jour la distance parcourue par le robot
        """
        if not self.stop() and not self.rob.estCrash:
            pos_actuelle = (self.rob.x, self.rob.y)
            self.parcouru = distance(self.pt_depart, pos_actuelle)
            time.sleep(REFRESH_DT)
            return self.step()

    def stop(self): 
        """ Détermine si on a bien parcouru la distance souhaitée
            :returns: True si on a bien complété la stratégie, False sinon
        """
        if self.parcouru >= self.distance :
            self.rob.setVitAng(0)
            self.rob.estSousControle = False
            return True
        return False


class StrategieTourner:
    
    def __init__(self, rob, angle):

        """ Stategie qui fait tourner le robot d'un angle donné
            :param rob: le robot que l'on veut faire tourner
            :param angle: la rotation que l'on veut ordonner au robot d'effectuer
        """

        self.rob = rob
        self.angle = angle
        self.angle_parcouru = 0
        self.dir_depart = self.rob.direction

    def start(self) :
        self.rob.estSousControle = True
        self.angle_parcouru = 0
        self.dir_depart = self.rob.direction
        self.rob.setVitAng(0)

        # On considère ici une rotation d'un angle alpha dans le sens horaire, c.à.d si positif on tourne vers la droite, sinon vers la gauche
        # On change les vitesses des deux roues, en leur donnant des vitesses opposées afin de tourner sur place
        if self.angle > 0 :
            self.rob.changeVitAngG(1/2)
            self.rob.changeVitAngD(-1/2)

        elif self.angle < 0 :
            self.rob.changeVitAngD(1)
            self.rob.changeVitAngG(-1)

        self.step()

    def step(self):

        """ Le step de la stratégie tourner, qui induit le mouvement si c'est le premier ou bien met a jour l'angle qui a été parcouru jusqu'à maintenant sinon
            :returns: ne retourne rien, on met juste a jour le paramètre distance parcourue
        """
        if not self.stop() and not self.rob.estCrash:
            self.angle_parcouru = getAngleFromVect(self.dir_depart, self.rob.direction)
            time.sleep(REFRESH_DT/10)
            return self.step()

    def stop(self) : 

        """ Détermine si on a fini de faire la rotation de l'angle self.angle
            :returns: True si la rotation a bien été effectuée, False sinon
        """
        if abs(self.angle_parcouru - self.angle) < 0.4 :
            self.rob.setVitAng(0)
            self.rob.estSousControle = False
            return True
        return False


class StrategieSeq:

    def __init__(self, listeStrat) :
        """ Statégie séquentielle
            :param listeStrat: liste de stratégies qui vont être executées à la suite
            :param indice: permet de parcourir la liste de stratégies
            :returns: rien, on initialise la stratégie séquentielle
        """
        self.listeStrat = listeStrat
        self.indice = -1
        #self.last_refresh = 0

    def start(self):
        self.indice = -1
        self.step()

    def step(self) : 
        """ Le step de la stratégie séquentielle, où on fait le step de la stratégie en cours ou on passe a la stratégie suivante selon le cas, et on met à jour le robot
            :returns: rien, il s'agit juste de lancement de sous-stratégies et de mise à jour de robots
        """
        if not self.stop() and not self.listeStrat[0].rob.estCrash:
            self.indice += 1
            self.last_refresh = 0
            self.listeStrat[self.indice].start()
            return self.step()
        
        """if (self.indice < 0 or self.listeStrat[self.indice].stop()) and self.indice != len(self.listeStrat)-1: # Si on n'a pas encore commencé à lancer les stratégies unitaire ou si la stratégie en cours est terminée, on avance à la stratégie suivante
            self.indice += 1
            self.last_refresh = 0
            self.listeStrat[self.indice].start()

        self.listeStrat[self.indice].step() # On fait le step de la stratégie en cours 

        now = time.time()
        if self.last_refresh == 0 :
            self.last_refresh = now
        duree = now - self.last_refresh
        
        self.listeStrat[self.indice].rob.refresh(duree) # On refresh le robot sur la durée qui s'est écoulée depuis le dernier rafraichissement
"""
    def stop(self) : 
        """ Détermine si la stratégie séquentielle est terminée, donc si toutes ses sous-stratégies son terminées 
            :returns: True si toutes les stratégies ont bien été accomplies, False sinon
        """
        return self.indice == len(self.listeStrat)-1 and self.listeStrat[self.indice].stop() 

