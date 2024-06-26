##### LU2IN013 
<div align="center">
      <h1> <img src="https://d29zukiv45njce.cloudfront.net/images/poli.png" width="90px"><br/>Projet S4 Mono-Info 💻</h1>
     </div>

[Rapport final](https://github.com/thibautmarcq/projet-2IN013/blob/main/autre/Rapport/Rapport_LU2IN013.pdf)       [Diapos Canva](https://www.canva.com/design/DAGG5gl8c54/ctSZ7vz2iyxrhtkZ1uaysg/edit?utm_content=DAGG5gl8c54&utm_campaign=designshare&utm_medium=link2&utm_source=sharebuttonhttps://www.canva.com/design/DAGG5gl8c54/ctSZ7vz2iyxrhtkZ1uaysg/edit?utm_content=DAGG5gl8c54&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

# Projet réalisé par
#### [@Inès BENAMER-BELKACEM](https://github.com/ines-benamer) [@Claude CHIBOUT](https://github.com/claudechibout) [@Maëlle LIU](https://github.com/maelleliu) [@Thibaut MARCQ](https://github.com/thibautmarcq) [@Jérôme YU](https://github.com/weeyu)

# Installation

```console
sudo apt-get install python3-tk
sudo apt-get install libasound-dev
```
```console
pip install tk
pip install panda3d
pip install simpleaudio
pip install opencv-python
```

# Objectifs
### Partie 1
- Réaliser une **interface** de **simulation** de notre robot avant de l'intégrer dans le monde réel
- Coder un ensemble de **stratégies** réalisables par le robot (**tracer un carré**, avancer jusqu'à une certaine **distance d'un obstacle**, effectuer une **stratégie séquentielle**)
- Coder des stratégies **conditionnelles** et de **boucle** pour le rendre Turing Complet

### Partie 2
###### Une fois notre robot simulé bien établi
- Implémenter les **stratégies simulées** sur le robot réel
- Créer une **interface 3D** de notre simulation
- **Reconnaître une balise** sur une image et **suivre cette balise** (dans l'interface 3D puis sur le robot réel)



# Stratégies
## Sur le robot réel
### Stratégie carré
https://github.com/thibautmarcq/projet-2IN013/assets/50046548/751b4a39-9b00-4900-a36d-10cb2c4f24e9
##### Pour un plus grand carré
https://github.com/thibautmarcq/projet-2IN013/assets/50046548/d3df6268-1612-4bac-b10d-dada63ef7b68

### Stratégie arrêt mur
https://github.com/thibautmarcq/projet-2IN013/assets/50046548/d2bb6471-b1d8-41ef-8c7e-251c583e65ec

### Stratégie suivre balise
https://github.com/thibautmarcq/projet-2IN013/assets/50046548/d1fde213-b679-43a9-abc9-974adfb3d7c5


## Sur le robot simulé
### Stratégie carré et collision dans un obstacle
#### Interface 2D
https://github.com/thibautmarcq/projet-2IN013/assets/50046548/feffbbbb-b789-4244-b766-514e5d33d84f
#### Interface 3D
https://github.com/thibautmarcq/projet-2IN013/assets/50046548/599a613e-95d2-4f37-b324-c134e6be1158

### Fonctionnalité supplémentaire
#### Notre robot peut se déplacer librement graces aux touches aze, qsd (dans les interfaces et dans le monde réel)
##### Exemple
https://github.com/thibautmarcq/projet-2IN013/assets/50046548/879f8fcd-3523-470f-a6ce-569f3e3a2665



# Divers :
<a href=https://trello.com/invite/b/sourGsMk/ATTI821518a3e67f2eee19cd581af1dc9cc4DB8D29A3/les-meilleurs-projet>Lien Trello
