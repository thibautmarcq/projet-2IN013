# pip install panda3d==1.10.14

from src.Robot.robot import Robot
from src.constantes import LONGUEUR_ROBOT, LARGEUR_ROBOT, TAILLE_ROUE, DICO_COULEURS

from direct.showbase.ShowBase import ShowBase
from direct.task import Task 
from panda3d.core import Point3, load_prc_file, GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomVertexWriter, Vec3, GeomNode

from math import sin, cos, pi
from time import sleep
from threading import Thread

load_prc_file('src/Interface3D/config.prc')

class Interface3D(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.nbRobots = 0
        
        self.createRobot("moulinex3D", 4, 5, LARGEUR_ROBOT, LONGUEUR_ROBOT, 15, TAILLE_ROUE, "lightblue")
        T_move = Thread(target=self.testMove, args=[0.05], daemon=True)
        T_move.start()
        T_update = Thread(target=self.testUpdate, daemon=True)
        T_update.start()
        # self.taskMgr.add(self.spinCameraTask, "spinCameraTask")
        self.taskMgr.add(self.updateCameraTask, "updateCameraTask")

    def testUpdate(self):
        while True:
            sleep(0.005)
            self.updateRobot(self.robot)

    def testMove(self, temps):
        sleep(12) # pour nous laisser le temps de positionner le robot
        while True:
            sleep(temps)
            self.robot.y+=1
            print('okayy')
    
    def createRobot(self, nom, x, y, width, length, height, rayonRoue, couleur):
        """Crée un robot en 3D (rectangle)
        	:param nom: nom du robot
			:param x: coordonnée x à laquelle on veut initialiser le robot
			:param y: coordonnée y à laquelle on veut initialiser le robot
			:param width: la largeur du robot
			:param length: la longueur du robot
            :param height: la hauteur du robot
			:param rayonRoue: la taille des roue
			:returns: ne retourne rien, ça initalise seulement le robot dans l'interface 3d
        """
        self.robot = Robot(nom, x, y, width, length, rayonRoue, couleur)
        self.robot.height = height
        self.robot.num = self.nbRobots
        self.nbRobots+=1
        
        # toutes les variables sont reliées à un robot, d'où le self.robot
        self.robot.format = GeomVertexFormat.getV3() # type des sommets
        self.robot.vdata = GeomVertexData("rectangle", self.robot.format, Geom.UHDynamic) # UHDynamic car les sommets vont devoir être bougés quand le robot va bouger
        self.robot.vertex = GeomVertexWriter(self.robot.vdata, "vertex")

        # Définition des sommets du robot | leur indice en comm (voir fiche thibo)
        self.robot.vertex.addData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)-(self.robot.length/2), 0)  # 0 dèrrière bas gauche
        self.robot.vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)-(self.robot.length/2), 0)  # 1 derriere bas droit
        self.robot.vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)+(self.robot.length/2), 0)  # 2 devant bas droit
        self.robot.vertex.addData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)+(self.robot.length/2), 0)  # 3 devant bas gauche
        self.robot.vertex.addData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)-(self.robot.length/2), self.robot.height)  # 4 derriere haut gauche
        self.robot.vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)-(self.robot.length/2), self.robot.height)  # 5 derriere haut droit
        self.robot.vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)+(self.robot.length/2), self.robot.height)  # 6 devant haut droit
        self.robot.vertex.addData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)+(self.robot.length/2), self.robot.height)  # 7 devant haut gauche

        # Création de l'objet (composition de triangles)
        self.robot.rectangle = GeomTriangles(Geom.UHDynamic)

        # Ajout des faces du carré
        # Bottom
        self.robot.rectangle.addVertices(0, 1, 2)
        self.robot.rectangle.addVertices(2, 3, 0)
        # Top
        self.robot.rectangle.addVertices(4, 5, 6)
        self.robot.rectangle.addVertices(6, 7, 4)
        # Front
        self.robot.rectangle.addVertices(0, 1, 5)
        self.robot.rectangle.addVertices(5, 4, 0)
        # Back
        self.robot.rectangle.addVertices(3, 2, 6)
        self.robot.rectangle.addVertices(6, 7, 3)
        # Left
        self.robot.rectangle.addVertices(0, 4, 7)
        self.robot.rectangle.addVertices(7, 3, 0)
        # Right
        self.robot.rectangle.addVertices(1, 2, 6)
        self.robot.rectangle.addVertices(6, 5, 1)
        
        # Créer un objet Geom (=l'objet du robot) pour contenir les triangles (=les faces)
        self.robot.geom = Geom(self.robot.vdata)
        self.robot.geom.addPrimitive(self.robot.rectangle)

        # Créer un nœud pour contenir le Geom
        self.robot.node = GeomNode("rectangle")
        self.robot.node.addGeom(self.robot.geom)

        # Créer un nœud de scène parent pour le nœud de géométrie
        self.robot.np = self.render.attachNewNode(self.robot.node) # np est le noeud de l'objet (=un ptr) dans le moteur graphique
        self.robot.np.setPos(0, 0, 0)  # Déplacer le triangle pour le voir
        
        self.robot.vectcouleur = DICO_COULEURS[self.robot.couleur]
        self.robot.np.setColor(self.robot.vectcouleur[0], self.robot.vectcouleur[1], self.robot.vectcouleur[2], self.robot.vectcouleur[3]) # RGB + transparence | COULEUR
        self.robot.np.setTwoSided(True) # pour render toutes les faces
    
    def updateRobot(self, robot):
        """ Update le visuel d'un robot dans l'interface
        :param robot: le robot pour lequel on veut update l'affichage
        :returns: rien, recalcule seulement les coo des sommets et update le visuel d'un robot
        """
        self.robot.vertex.setRow(0)
        self.robot.vertex.setData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)-(self.robot.length/2), 0)  # 0 dèrrière bas gauche
        self.robot.vertex.setRow(1)
        self.robot.vertex.setData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)-(self.robot.length/2), 0)  # 1 derriere bas droit
        self.robot.vertex.setRow(2)
        self.robot.vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)+(self.robot.length/2), 0)  # 2 devant bas droit
        self.robot.vertex.setRow(3)
        self.robot.vertex.setData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)+(self.robot.length/2), 0)  # 3 devant bas gauche
        self.robot.vertex.setRow(4)
        self.robot.vertex.setData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)-(self.robot.length/2), self.robot.height)  # 4 derriere haut gauche
        self.robot.vertex.setRow(5)
        self.robot.vertex.setData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)-(self.robot.length/2), self.robot.height)  # 5 derriere haut droit
        self.robot.vertex.setRow(6)
        self.robot.vertex.setData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)+(self.robot.length/2), self.robot.height)  # 6 devant haut droit
        self.robot.vertex.setRow(7)
        self.robot.vertex.setData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)+(self.robot.length/2), self.robot.height)  # 7 devant haut gauche
    
    # Task pour faire rotate la camera
    def spinCameraTask(self, task):
        """ Effectue une rotation de la caméra autour du robot pendant qu'il avance """
        angleDegrees = task.time * 30.0
        angleRadians = angleDegrees * (pi / 180.0)
        radius = 300
        camera_x = self.robot.x + radius * cos(angleRadians)
        camera_y = self.robot.y + radius * sin(angleRadians)
        self.camera.setPos(camera_x, camera_y, 200)  # Élever la caméra
        self.camera.lookAt(Point3(self.robot.x, self.robot.y, 0))
        return Task.cont
    
    # Task pour suivre le robot
    def updateCameraTask(self, task):
        """ Set la caméra derrière le robot et le suit pendant qu'il avance """
        # Set the camera position relative to the robot's position
        self.camera.setPos(self.robot.x - 150, self.robot.y - 200, 150)
        self.camera.lookAt(Point3(self.robot.x, self.robot.y, 0))
        
        return Task.cont  # Continue the task indefinitely

app = Interface3D()
app.run()