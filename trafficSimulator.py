# Importo librerie
import pygame
from grafica import *
import random



# Carico Immagini
car1img = pygame.image.load('imgGame\\auto.png')
car2img = pygame.image.load('imgGame\\auto2.png')
auto1 = pygame.transform.scale(car1img, (93, 46))
auto2 = pygame.transform.scale(car2img, (93, 46))


# Costanti Globale

Centro = (512, 384)
listacar = list()
LaneCoordinate = [[26, 500], [966, 220], [390, 16], [590, 730]]
LaneCentrali = [[460, 16], [966, 316], [526, 730], [26, 420]]
EndCoordinate = [[26, 220], [590, 16], [390, 730], [966, 500], [526, 16]]
a = []


class Car():
    def __init__(self):
        self.randomlane = random.choice([LaneCentrali, LaneCoordinate])
        self.initcoordinate = random.choice(self.randomlane)
        self.x = self.initcoordinate[0]
        self.y = self.initcoordinate[1]
        self.image = random.choice([auto1, auto2])
        if self.x == 966:
            self.image = pygame.transform.rotate(self.image, 180)
        if self.x == 390 or self.x == 460:
            self.image = pygame.transform.rotate(self.image, -90)
        if self.x == 590 or self.x == 526:
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.angle = 0
        self.speedx = 2
        self.speedy = 2
        self.saved_image = self.image.copy()
        self.pos = (self.x, self.y)
        self.startpos = None
        self.lane = None
        self.arrivo = None
        self.ingombro = None


    def randomCoordinateEND(self):
        a = [x for x in EndCoordinate if x[0] !=
             self.initcoordinate[0] and x[1] != self.initcoordinate[1]]
        self.endcoordinate = random.choice(a)
        self.arrivox, self.arrivoy = self.endcoordinate[0], self.endcoordinate[1]
        # self.arrivoy = self.endcoordinate[1]

    def checklane(self):
        if self.startpos == 'destra' or self.startpos == 'sinistra':
            if abs(self.initcoordinate[1]-Centro[1]) > 115:
                self.lane = 'esterna'
            else:
                self.lane = 'centro'
        if self.startpos == 'alto' or self.startpos == 'basso':
            if abs(self.initcoordinate[0]-Centro[0]) > 70:
                self.lane = 'esterna'
            else:
                self.lane = 'centro'

    def changelane(self):  # interno esterno
        if self.startpos == 'destra' or self.startpos == 'sinistra':
            # si sta muovendo
            if self.lane != 'esterna' and self.initcoordinate[0] != self.x:
                if Centro[1] > self.initcoordinate[1]:  # alto a alto destra
                    if abs(self.y - Centro[1]) < 164:
                        self.y -= self.speedy
                elif Centro[1] < self.initcoordinate[1]:  # basso a basso destra
                    if abs(self.y - Centro[1]) < 116:
                        self.y += self.speedy
        if self.startpos == 'alto' or self.startpos == 'basso':
            # si sta muovendo
            if self.lane != 'esterna' and self.initcoordinate[1] != self.y:
                if Centro[0] > self.initcoordinate[0]:  # alto a alto destra
                    if abs(self.x - Centro[0]) < 122:
                        self.x -= self.speedx
                elif Centro[0] < self.initcoordinate[0]:  # basso a basso destra
                    if abs(self.x - Centro[0]) < 78:
                        self.x += self.speedx

    def changelanerevers(self):  # esterno interno
        if self.startpos == 'destra' or self.startpos == 'sinistra':
            # si sta muovendo
            if self.lane == 'esterna' and self.initcoordinate[0] != self.x:
                if Centro[1] > self.initcoordinate[1]:  # destra
                    if abs(self.y - Centro[1]) > 70:
                        self.y += self.speedy
                elif Centro[1] < self.initcoordinate[1]:  # sinistra
                    if abs(self.y - Centro[1]) > 48:
                        self.y -= self.speedy
        if self.startpos == 'alto' or self.startpos == 'basso':
            # si sta muovendo
            if self.lane == 'esterna' and self.initcoordinate[1] != self.y:
                if Centro[0] > self.initcoordinate[0]:  # alto
                    if abs(self.x - Centro[0]) > 52:
                        self.x += self.speedx
                elif Centro[0] < self.initcoordinate[0]:  # basso
                    if abs(self.x - Centro[0]) > 12:
                        self.x -= self.speedx

    def percorsoArrivo(self):

        # alto
        if self.arrivox > Centro[0] and self.arrivoy < Centro[1]:
            if self.startpos == 'basso':
                self.y -= self.speedy
            self.arrivo = 'alto'
        # destra
        if self.arrivox > Centro[0] and self.arrivoy > Centro[1]:
            if self.startpos == 'sinistra':
                self.x += self.speedx
            self.arrivo = 'destra'
        # sinistra
        if self.arrivox < Centro[0] and self.arrivoy < Centro[1]:
            if self.startpos == 'destra':
                self.x -= self.speedx
            self.arrivo = 'sinistra'
        # basso
        if self.arrivox < Centro[0] and self.arrivoy > Centro[1]:
            if self.startpos == 'alto':
                self.y += self.speedy
            self.arrivo = 'basso'

    def definestarpos(self):
        # ritorna sia corsia centrale o esterna più quadrante
        # destra
        if self.initcoordinate[0] > Centro[0] and self.initcoordinate[1] < Centro[1]:
            self.startpos = 'destra'
        # basso
        if self.initcoordinate[0] > Centro[0] and self.initcoordinate[1] > Centro[1]:
            self.startpos = 'basso'
        # alto
        if self.initcoordinate[0] < Centro[0] and self.initcoordinate[1] < Centro[1]:
            self.startpos = 'alto'
        # sinistra
        if self.initcoordinate[0] < Centro[0] and self.initcoordinate[1] > Centro[1]:
            self.startpos = 'sinistra'
        self.checklane()
    def rotatedx(self,angle):
        self.image = pygame.transform.rotate(self.saved_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle -= angle
    def rotatesx(self,angle):
        self.image = pygame.transform.rotate(self.saved_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle += angle
    def move(self):
        self.pos = (self.x, self.y)
        self.percorsoArrivo()
        if self.startpos == 'alto' and self.arrivo == 'sinistra':
            if self.y < self.arrivoy:
                self.y += self.speedy
            if self.y == self.arrivoy and self.angle != -95:
                self.rotatedx(5)
            if self.angle == -95:
                if self.x > self.arrivox:
                    self.x -= self.speedx
            if self.lane == 'centro':
                self.changelane()
        if self.startpos == 'alto' and self.arrivo == 'destra':
            if self.y < self.arrivoy:
                self.y += self.speedy
            if self.y == self.arrivoy and self.angle != 95:
                self.rotatesx(5)
            if self.angle == 95:
                if self.x < self.arrivox:
                    self.x += self.speedx
            if self.lane == 'esterna':
                self.changelanerevers()
        if self.startpos == 'basso' and self.arrivo == 'sinistra':
            if self.y > self.arrivoy:
                self.y -= self.speedy
            if self.y == self.arrivoy and self.angle != 95:
                self.rotatesx(5)
            if self.angle == 95:
                if self.x > self.arrivox:
                    self.x -= self.speedx
            if self.lane == 'esterna':
                self.changelanerevers()
        if self.startpos == 'basso' and self.arrivo == 'destra':
            if self.y > self.arrivoy:
                self.y -= self.speedy
            if self.y == self.arrivoy and self.angle != -95:
                self.rotatedx(5)
            if self.angle == -95:
                if self.x < self.arrivox:
                    self.x += self.speedx
            if self.lane == 'centro':
                self.changelane()

        if self.startpos == 'sinistra' and self.arrivo == 'alto':
            if self.x < self.arrivox:
                self.x += self.speedx
            if self.x == self.arrivox and self.angle != 95:
                self.rotatesx(5)
            if self.angle == 95:
                if self.y > self.arrivoy:
                    self.y -= self.speedy
            if self.lane == 'esterna':
                self.changelanerevers()
        if self.startpos == 'sinistra' and self.arrivo == 'basso':
            if self.x < self.arrivox:
                self.x += self.speedx
            if self.x == self.arrivox and self.angle != -95:
                self.rotatedx(5)
            if self.angle == -95:
                if self.y < self.arrivoy:
                    self.y += self.speedy
            if self.lane == 'centro':
                self.changelane()
        if self.startpos == 'destra' and self.arrivo == 'alto':
            if self.x > self.arrivox:
                self.x -= self.speedx
            if self.x == self.arrivox and self.angle != -95:
                self.rotatedx(5)
            if self.angle == -95:
                if self.y > self.arrivoy:
                    self.y -= self.speedy
            if self.lane == 'centro':
                self.changelane()
        if self.startpos == 'destra' and self.arrivo == 'basso':
            if self.x > self.arrivox:
                self.x -= self.speedx
            if self.x == self.arrivox and self.angle != 95:
                self.rotatesx(5)
            if self.angle == 95:
                if self.y < self.arrivoy:
                    self.y += self.speedy
            if self.lane == 'esterna':
                self.changelanerevers()




def inizializza(Numerocars):
    global listacar
    for n in range(Numerocars):
        a = Car()
        a.definestarpos()
        a.checklane()
        a.lane
        a.randomCoordinateEND()
        listacar.append(a)

 
inizializza(1)
# initcordinate solo per test
x = 0
y = 0
dsds = 0


def checkCollision(T):

    for i in range(len(T) - 1):
        for j in range(i + 1, len(T)):
            if T[i].ingombro.colliderect(T[j].ingombro):
                T[i].speedx = 0
                T[i].speedy = 0
                T[j].speedx = 0
                T[j].speedy = 0
                # return 1
    return 0

while True:
     
    disegna_oggetti(listacar,textsurface,textsurface2)
    for car in listacar:
        car.move()
        car.ingombro = pygame.Rect(car.x, car.y, car.rect[2], car.rect[3])
        # rimuovo le auto che sono arrivate a destinazione
        if car.arrivox == car.x and car.arrivoy == car.y:
            listacar.remove(car)
    textsurface2 = myfont.render('start'+str(listacar[0].ingombro), False, (0, 0, 0))
    textsurface = myfont.render('collisioni'+str(dsds), False, (0, 0, 0))
    dsds += checkCollision(listacar)
    aggiorna()

    for event in pygame.event.get():
        # Per ricevere coordinate sulla poszione del mouse
        # x, y = pygame.mouse.get_pos()
        # print("X : {} Y: {}".format(x, y))
        # per inizializzare macchina con click
        if event.type == pygame.MOUSEBUTTONUP:
            inizializza(1)
            print("click")
        if event.type == pygame.QUIT:  # gestisco la chiusura della finestra
            pygame.quit()
            SystemExit
