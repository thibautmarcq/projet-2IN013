# pip install panda3d==1.10.14

from src.Robot.robot import Adaptateur_simule
from src.constantes import LONGUEUR_ROBOT, LARGEUR_ROBOT, TAILLE_ROUE, HAUTEUR_ROBOT, DICO_COULEURS, LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1
from src.environnement import Environnement

from direct.showbase.ShowBase import ShowBase
from direct.task import Task 
from panda3d.core import Point3, load_prc_file, GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomVertexWriter, Vec3, GeomNode

from math import sin, cos, pi
from time import sleep
from threading import Thread

load_prc_file('src/Interface3D/config.prc')

class Interface3D(ShowBase):

    def __init__(self, env):
        ShowBase.__init__(self)
        # self.nbRobots = 0
        self.env = env
        self.createAllRobots()
        self.createEnvironnement()
        
        # robot = Robot("moulinex3D", 4, 5, LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE, "lightblue")
        # self.env.addRobot(robot)
        
        T_move = Thread(target=self.testMove, args=[self.env.listeRobots[0], 0.05], daemon=True)
        T_move.start()
        T_update = Thread(target=self.testUpdate, args=[self.env.listeRobots[0]], daemon=True)
        T_update.start()
        # self.taskMgr.add(self.spinCameraTask, "spinCameraTask")
        # self.taskMgr.add(self.updateCameraTask, "updateCameraTask")

    def testUpdate(self, robot):
        while True:
            sleep(0.005)
            self.updateRobot(robot)

    def testMove(self, robotA, temps):
        robot = robotA.robot
        sleep(12) # pour nous laisser le temps de positionner le robot
        while True:
            sleep(temps)
            robot.y+=1
            print('okayy - ', robot.y)
            
    def createAllRobots(self):
        """ Crée tous les robots présents dans l'environnement
        :returns: rien, va seulement créer tous les robots de l'environnement (en attribut de l'interface)
        """
        for robA in self.env.listeRobots:
            self.createRobot(robA)
    
    def createRobot(self, robotA):
        """Crée un robot en 3D (rectangle) dans l'interface
        :param robotA: adaptateur de robot
		:returns: ne retourne rien, ça initalise seulement le robot dans l'interface 3d
        """
        robot = robotA.robot
        
        # toutes les variables sont reliées à un robot
        robot.format = GeomVertexFormat.getV3() # type des sommets
        robot.vdata = GeomVertexData("rectangle", robot.format, Geom.UHDynamic) # UHDynamic car les sommets vont devoir être bougés quand le robot va bouger
        robot.vertex = GeomVertexWriter(robot.vdata, "vertex")

        # Définition des sommets du robot | leur indice en comm (voir fiche thibo)
        robot.vertex.addData3f((robot.x)-(robot.width/2), (robot.y)-(robot.length/2), 0)  # 0 dèrrière bas gauche
        robot.vertex.addData3f((robot.x)+(robot.width/2), (robot.y)-(robot.length/2), 0)  # 1 derriere bas droit
        robot.vertex.addData3f((robot.x)+(robot.width/2), (robot.y)+(robot.length/2), 0)  # 2 devant bas droit
        robot.vertex.addData3f((robot.x)-(robot.width/2), (robot.y)+(robot.length/2), 0)  # 3 devant bas gauche
        robot.vertex.addData3f((robot.x)-(robot.width/2), (robot.y)-(robot.length/2), robot.height)  # 4 derriere haut gauche
        robot.vertex.addData3f((robot.x)+(robot.width/2), (robot.y)-(robot.length/2), robot.height)  # 5 derriere haut droit
        robot.vertex.addData3f((robot.x)+(robot.width/2), (robot.y)+(robot.length/2), robot.height)  # 6 devant haut droit
        robot.vertex.addData3f((robot.x)-(robot.width/2), (robot.y)+(robot.length/2), robot.height)  # 7 devant haut gauche

        # Création de l'objet (composition de triangles)
        robot.rectangle = GeomTriangles(Geom.UHDynamic)

        # Ajout des faces du carré
        # Bottom
        robot.rectangle.addVertices(0, 1, 2)
        robot.rectangle.addVertices(2, 3, 0)
        # Top
        robot.rectangle.addVertices(4, 5, 6)
        robot.rectangle.addVertices(6, 7, 4)
        # Front
        robot.rectangle.addVertices(0, 1, 5)
        robot.rectangle.addVertices(5, 4, 0)
        # Back
        robot.rectangle.addVertices(3, 2, 6)
        robot.rectangle.addVertices(6, 7, 3)
        # Left
        robot.rectangle.addVertices(0, 4, 7)
        robot.rectangle.addVertices(7, 3, 0)
        # Right
        robot.rectangle.addVertices(1, 2, 6)
        robot.rectangle.addVertices(6, 5, 1)
        
        # Créer un objet Geom (=l'objet du robot) pour contenir les triangles (=les faces)
        robot.geom = Geom(robot.vdata)
        robot.geom.addPrimitive(robot.rectangle)

        # Créer un nœud pour contenir le Geom
        robot.node = GeomNode("rectangle")
        robot.node.addGeom(robot.geom)

        # Créer un nœud de scène parent pour le nœud de géométrie
        robot.np = self.render.attachNewNode(robot.node) # np est le noeud de l'objet (=un ptr) dans le moteur graphique
        robot.np.setPos(0, 0, 0)  # Déplacer le triangle pour le voir
        
        robot.vectcouleur = DICO_COULEURS[robot.couleur]
        robot.np.setColor(robot.vectcouleur[0], robot.vectcouleur[1], robot.vectcouleur[2], robot.vectcouleur[3]) # RGB + transparence | COULEUR
        robot.np.setTwoSided(True) # pour render toutes les faces
    
    def updateRobot(self, robotA):
        """ Update le visuel d'un robot dans l'interface
        :param robotA: le robotA pour lequel on veut update l'affichage
        :returns: rien, recalcule seulement les coo des sommets et update le visuel d'un robot
        """
        robot = robotA.robot
        robot.vertex.setRow(0)
        robot.vertex.setData3f((robot.x)-(robot.width/2), (robot.y)-(robot.length/2), 0)  # 0 dèrrière bas gauche
        robot.vertex.setRow(1)
        robot.vertex.setData3f((robot.x)+(robot.width/2), (robot.y)-(robot.length/2), 0)  # 1 derriere bas droit
        robot.vertex.setRow(2)
        robot.vertex.addData3f((robot.x)+(robot.width/2), (robot.y)+(robot.length/2), 0)  # 2 devant bas droit
        robot.vertex.setRow(3)
        robot.vertex.setData3f((robot.x)-(robot.width/2), (robot.y)+(robot.length/2), 0)  # 3 devant bas gauche
        robot.vertex.setRow(4)
        robot.vertex.setData3f((robot.x)-(robot.width/2), (robot.y)-(robot.length/2), robot.height)  # 4 derriere haut gauche
        robot.vertex.setRow(5)
        robot.vertex.setData3f((robot.x)+(robot.width/2), (robot.y)-(robot.length/2), robot.height)  # 5 derriere haut droit
        robot.vertex.setRow(6)
        robot.vertex.setData3f((robot.x)+(robot.width/2), (robot.y)+(robot.length/2), robot.height)  # 6 devant haut droit
        robot.vertex.setRow(7)
        robot.vertex.setData3f((robot.x)-(robot.width/2), (robot.y)+(robot.length/2), robot.height)  # 7 devant haut gauche
        
        
    def createEnvironnement(self):
        """ Crée le visuel de l'environnement dans l'interface
        :returns: rien, crée simplement l'environnement en 3D 
        """
        self.env.format = GeomVertexFormat.getV3()
        self.env.vdata = GeomVertexData("envi", self.env.format, Geom.UHStatic)
        self.env.vertex = GeomVertexWriter(self.env.vdata, "vertex")
        # Définition des sommets
        # 2 --- 3
        # 0 --- 1
        self.env.vertex.addData3f(0, 0, -1) # 0 bas gauche
        self.env.vertex.addData3f(self.env.length, 0, -1) # 1 bas droite
        self.env.vertex.addData3f(0, self.env.width, -1) # 2 haut gauche
        self.env.vertex.addData3f(self.env.length, self.env.width, -1) # 3 haut droit
        # Création de l'objet + ajout du plan
        self.env.plan = GeomTriangles(Geom.UHStatic)
        self.env.plan.addVertices(0, 1, 2)
        self.env.plan.addVertices(1, 3, 2)
        # Link des données
        self.env.geom = Geom(self.env.vdata)
        self.env.geom.addPrimitive(self.env.plan)
        # Création noeud + ajout noeud dans le render
        self.env.node = GeomNode("envi")
        self.env.node.addGeom(self.env.geom)
        self.env.np = self.render.attachNewNode(self.env.node)
        self.env.np.setPos(0,0,-1)
        self.env.np.setColor(1,1,1,1) #blanc
        self.env.np.setTwoSided(True)
            
        
    
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

# ----- MAIN -----

envi = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)
robot = Adaptateur_simule("moulinex3D", 4, 5, LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE, envi, "lightblue")
envi.addRobot(robot)
envi.addRobot
app = Interface3D(envi)
app.run()