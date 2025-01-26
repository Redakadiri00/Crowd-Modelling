import matplotlib.pyplot as plt 
import numpy as np 
import math
import random
import pickle
from matplotlib.patches import Rectangle
import matplotlib.animation as animation


#initialisation
nombrePietons = 20
largeurSalle = 5
longueurSalle = 5
k = 1.2 * (10**3)
h = 10**(-1.5) #pas du temps 
THO = 0.5 #temps de relaxation
listePorte = [[largeurSalle, longueurSalle/2]] 
Vn = np.zeros((nombrePietons,2)) #vitesse initial

#génération des coordonnées aléatoires des piétons
coordonnees = np.zeros((nombrePietons,2))
for i in range(nombrePietons):
    coordonnees[i,0] = (random.uniform(0,largeurSalle))
    coordonnees[i,1] = (random.uniform(0,largeurSalle))
    
#génération des vitesses souhaitées aléatoires entre 1.1m/s et 1.48 m/s
vitesseSouhaitee = np.zeros(nombrePietons)
for i in range(nombrePietons):
    vitesseSouhaitee[i] = random.uniform(1.1,1.48)    

#génération des masses aléatoires entre 50kg et 100kg
masse = np.random.randint(low=50, high=100, size=nombrePietons)

#choix des rayons convenables des pietons entre 0.2m et 0.25m
rayon = np.array([0.001 * masse[i] + 0.15 for i in range(nombrePietons)])
#listes des couleurs choisi pour représenter chaque piéton
t = 'tab:'
colors = ['b', 'g', 'r', 'c', 'm', 'y', t+'blue', t+'orange', 'limegreen', 'limegreen', 'orangered', t+'purple', t+'brown', t+'pink', t+'grey', 'aquamarine', 'lime', 'yellow', 'pink', 'indigo', 'gold']

fig, ax = plt.subplots()

#définition des fonctions:
#calcul de la distance entre le piéton et la porte
def Distance_porte(numeroPieton, coordsPorte):
    return math.sqrt((coordsPorte[0]-coordonnees[numeroPieton][0])**2 + (coordsPorte[1]-coordonnees[numeroPieton][1])**2)

#détermination de la porte la plus proche
def PortePlusProche(numeroPieton,listePorte):
    distances = []
    for p in range(0,len(listePorte)):
        distances.append(Distance_porte(numeroPieton,listePorte[p]))
    return distances.index(min(distances))

#calcul de la direction souhaitée d'un pieton (vers la plus proche porte)
def direction(numeroPieton):
    porte = PortePlusProche(numeroPieton,listePorte)
    X = listePorte[porte][0] - coordonnees[numeroPieton][0]
    Y = listePorte[porte][1] - coordonnees[numeroPieton][1]
    return np.array([X / Distance_porte(numeroPieton,listePorte[porte]), Y / Distance_porte(numeroPieton,listePorte[porte])])

#calcul de la force motrice Fid
def ForceMotrice_Fid(numeroPieton,Vn):
    dir = direction(numeroPieton)
    return (masse[numeroPieton] * (vitesseSouhaitee[numeroPieton] * dir - Vn[numeroPieton])) / THO

#calcul de la distance entre deux piétons
def distanceEntre(i,j,coordonnees):
    return math.sqrt((coordonnees[i][0]-coordonnees[j][0])**2 + (coordonnees[i][1]-coordonnees[j][1])**2)

#détection des piétons en contact avec un piéton
def detectionContact(i,coordonnees):
    pietonsTouches = []
    for j in range(0,nombrePietons): #j pour les autres piétons
        if j != i:
            Dij = distanceEntre(i,j,coordonnees) - (rayon[i] + rayon[j]) 
            if Dij <= 0:
                pietonsTouches.append(j)
    return pietonsTouches

#calcul de la force pieton-pieton G
def Force_G(numeroPieton,coordonnees):
    pietonsTouches = detectionContact(numeroPieton,coordonnees)
    G = np.zeros(2)
    for j in pietonsTouches:
        Dij = distanceEntre(numeroPieton,j,coordonnees) - (rayon[numeroPieton] + rayon[j])
        G = G + k * Dij * ((coordonnees[j] - coordonnees[numeroPieton]) / distanceEntre(j,numeroPieton,coordonnees))
    return G 

#calcul de la force pieton-mur de la porte K
def Force_K(numeroPieton,coordonnees):
    porte = PortePlusProche(numeroPieton, listePorte)
    K = np.zeros(2)
    if coordonnees[numeroPieton,1] < listePorte[porte][1] - 0.2 or coordonnees[numeroPieton,1] > listePorte[porte][1] + 0.2:
        D = largeurSalle - coordonnees[numeroPieton,0] - rayon[numeroPieton]
        if D < 0 :
            K[0] = K[0] + k * D 
    return K 

#calcul de la vitesse d'un piéton à tout instant
def calculVitesse(numeroPieton,Vn,coordonnees):
    return Vn[numeroPieton] + (h / masse[numeroPieton]) * (ForceMotrice_Fid(numeroPieton,Vn) + Force_G(numeroPieton,coordonnees) + Force_K(numeroPieton,coordonnees))

#calcul de la position d'un piéton à tout instant
def calculPosition (numeroPieton,Vn,coordonnees):
    return coordonnees[numeroPieton] + h * Vn[numeroPieton]

#placement des objets (les tables)
coordonneesObj = [] #liste des coordonnees des objets
for i in np.arange(1,5,1):
    coordonneesObj = coordonneesObj + [(j,i) for j in np.arange(0.5,5.5,1)] 
        
#coordonnées initiales des etudiants dans la classe
coordonnees = np.zeros((nombrePietons,2))
for i in range(nombrePietons):
    coordonnees[i,0] = coordonneesObj[i][0]
    coordonnees[i,1] = coordonneesObj[i][1] + 0.2 

#définition des fonctions

#calcul de la distance entre le piéton et l'objet
def distanceEntreObj(i,j,coordonnees,coordObjets):
    return math.sqrt((coordonnees[i][0] - coordObjets[j][0])**2 + (coordonnees[i][1] - coordObjets[j][1])**2)

#détection des objets en contact avec un piéton
def detectionContactObjets(i,coordonnees,coordObjets):
    objetsTouches = []
    for j in range(0,nombrePietons): #j pour les objets (car nombrePietons=nombreObjets)
            Dij = distanceEntreObj(i,j,coordonnees,coordObjets) - 2 * rayon[i]
            if Dij <= 0 :
                objetsTouches.append(j)
    return objetsTouches     

#calcul de la force pieton-objet L
def Force_L(numeroPieton,coordonnees,coordObjets):
    objetsTouches = detectionContactObjets(numeroPieton,coordonnees,coordObjets)
    L = np.zeros(2)
    for j in objetsTouches:
        Dij = distanceEntreObj(numeroPieton,j,coordonnees,coordObjets) - 2 * rayon[numeroPieton]
        L = L + k * Dij * ((coordObjets[j] - coordonnees[numeroPieton]) / distanceEntreObj(numeroPieton,j,coordonnees,coordObjets))
    return L

#calcul de la vitesse d'un piéton à tout instant (en ajoutant la force L)
def calculVitesse(numPieton,Vn,coordonnees,coordObjets):
    return Vn[numPieton] + (h / masse[numPieton]) * (ForceMotrice_Fid(numPieton,Vn) + Force_G(numPieton,coordonnees) + Force_K(numPieton,coordonnees) + Force_L(numPieton,coordonnees,coordObjets))

def environnement():
    ax.plot()
    plt.axis('square')
    plt.xlim([0,largeurSalle]); plt.ylim([0,longueurSalle])
    plt.xlabel('Coordonnées en x') ; plt.ylabel('Coordonnées en y')
    for i in coordonneesObj:
        ax.add_patch(Rectangle((i[0]-0.1, i[1]-0.1),0.2,0.2))
    plt.scatter(listePorte[0][0]+0.1,listePorte[0][1], color = 'pink', marker = 's',edgecolors = 'r', s=400, label='Porte')
    plt.text(listePorte[0][0], listePorte[0][1],"Porte")

#traçage des positions des étudiants
def tracage():
    for N in range(0,nombrePietons):         
        plt.scatter(coordonnees[N,0],coordonnees[N,1],facecolors='none',edgecolors=colors[N],s=rayon[N]*200)

environnement()
for N in range(0,nombrePietons):
    plt.text(coordonnees[N][0],coordonnees[N][1], str(N+1))

for i in coordonneesObj:
    ax.add_patch(Rectangle((i[0]-0.1, i[1]-0.1),0.2,0.2))

def update(frame):
    for N in range(0,nombrePietons):
        if coordonnees[N,0]<listePorte[0][0]:
            Vn[N]=calculVitesse(N,Vn,coordonnees, coordonneesObj)
            coordonnees[N]=calculPosition(N,Vn,coordonnees)
        else:
            coordonnees[N]=np.array([1000,1000])
    tracage()

ani = animation.FuncAnimation(fig=fig, func=update, frames=40, interval=10)
plt.show()

