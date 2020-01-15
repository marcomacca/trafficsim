import random
import pygame

# Coordinate
Centro = (804, 464)
EndCoordinate = [[26, 306], [26, 406], [940, 16], [834, 16],
                 [630, 976], [730, 976], [1546, 584], [1546, 684]]
LaneCoordinate = [[26, 584], [1546, 306], [756, 16], [940, 976]]
LaneCentrali = [[728, 16], [1546, 396], [834, 976], [26, 490]]


# Carico Immagini
car1img = pygame.image.load('imgGame\\auto.png')
car2img = pygame.image.load('imgGame\\auto2.png')
truckimg = pygame.image.load('imgGame\\truck.png')

auto1 = pygame.transform.scale(car1img, (68, 33))
auto2 = pygame.transform.scale(car2img, (68, 33))
truck = pygame.transform.scale(truckimg, (100, 50))
# % di uscita di auto su auto2 su truck 40,40,20
population = [auto1, auto2, truck]
weights = [0.4, 0.4, 0.2]


class Car():
    def __init__(self):
        self.randomlane = random.choice([LaneCentrali, LaneCoordinate])
        self.initcoordinate = random.choice(self.randomlane)
        self.x, self.y = self.initcoordinate[0], self.initcoordinate[1]
        # in uscita ho un array perciò prendo [0]
        self.image = random.choices(population, weights)[0]
        if self.x == 1546:
            self.image = pygame.transform.rotate(self.image, 180)
        if self.x == 756 or self.x == 728:
            self.image = pygame.transform.rotate(self.image, -90)
        if self.x == 940 or self.x == 834:
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.angle = 0
        self.speedx = 2
        self.speedy = 2
        self.arrived = False
        self.saved_image = self.image.copy()
        self.pos = (self.x, self.y)
        self.startpos = None
        self.lane = None
        self.arrivo = None
        self.ingombro = pygame.Rect(self.pos, self.image.get_size())
        self.visione = None
        self.direzione = None
        self.definestarpos()
        self.checklane()
        self.lane
        self.randomCoordinateEND()
        self.percorsoArrivo()
        self.creavisione()

    def randomCoordinateEND(self):
        cordinate = [x for x in EndCoordinate if x[0] !=
                     self.initcoordinate[0] and x[1] != self.initcoordinate[1]]
        self.endcoordinate = random.choice(cordinate)
        self.arrivox, self.arrivoy = self.endcoordinate[0], self.endcoordinate[1]
        # self.arrivoy = self.endcoordinate[1]

    def checklane(self):
        if self.startpos == 'destra' or self.startpos == 'sinistra':
            if abs(self.initcoordinate[1]-Centro[1]) > 100:
                self.lane = 'esterna'
            else:
                self.lane = 'centro'
        if self.startpos == 'alto' or self.startpos == 'basso':
            if abs(self.initcoordinate[0]-Centro[0]) > 100:
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
                    if abs(self.x - Centro[0]) < 164:
                        self.x -= self.speedx
                elif Centro[0] < self.initcoordinate[0]:  # basso a basso destra
                    if abs(self.x - Centro[0]) < 140:
                        self.x += self.speedx

    def changelanerevers(self):  # esterno interno
        if self.startpos == 'destra' or self.startpos == 'sinistra':
            # si sta muovendo
            if self.lane == 'esterna' and self.initcoordinate[0] != self.x:
                if Centro[1] > self.initcoordinate[1]:  # destra
                    if abs(self.y - Centro[1]) > 70:
                        self.y += self.speedy
                elif Centro[1] < self.initcoordinate[1]:  # sinistra
                    if abs(self.y - Centro[1]) > 30:
                        self.y -= self.speedy
        if self.startpos == 'alto' or self.startpos == 'basso':
            # si sta muovendo
            if self.lane == 'esterna' and self.initcoordinate[1] != self.y:
                if Centro[0] > self.initcoordinate[0]:  # alto
                    if abs(self.x - Centro[0]) > 70:
                        self.x += self.speedx
                elif Centro[0] < self.initcoordinate[0]:  # basso
                    if abs(self.x - Centro[0]) > 32:
                        self.x -= self.speedx

    def anticollisione(self, listacar):
        collide = False
        for n in listacar:
            if self.visione.colliderect(n.ingombro):
                self.speedy = 0
                self.speedx = 0
                collide = True
            # se collidono le cancello per risolvere lo spawn di due auto nello stesso punto
            if self.ingombro.colliderect(n.ingombro):
                self.arrived = True
            if not collide:
                self.speedy = 2
                self.speedx = 2
                collide = False

    def controllosemaforo(self, listasemafori):
        collide = False
        for s in listasemafori:
            if s.colore == 'red':
                if self.ingombro.colliderect(s.rect):
                    self.speedy = 0
                    self.speedx = 0
                    break
            elif s.colore == 'yellow':
                if self.visione.colliderect(s.rect):
                    self.speedy = 1
                    self.speedx = 1
                    break
            elif s.colore == 'green':
                if self.visione.colliderect(s.rect):
                    self.speedy = 2
                    self.speedx = 2
                    break

    def percorsoArrivo(self):

        # alto
        if self.arrivox > Centro[0] and self.arrivoy < Centro[1]:
            if self.startpos == 'basso':
                self.y -= self.speedy
            self.arrivo = 'alto'
            self.direzione = 'su'
        # destra
        if self.arrivox > Centro[0] and self.arrivoy > Centro[1]:
            if self.startpos == 'sinistra':
                self.x += self.speedx
            self.arrivo = 'destra'
            self.direzione = 'destra'
        # sinistra
        if self.arrivox < Centro[0] and self.arrivoy < Centro[1]:
            if self.startpos == 'destra':
                self.x -= self.speedx
            self.arrivo = 'sinistra'
            self.direzione = 'sinistra'

        # basso
        if self.arrivox < Centro[0] and self.arrivoy > Centro[1]:
            if self.startpos == 'alto':
                self.y += self.speedy
            self.arrivo = 'basso'
            self.direzione = 'giù'

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

    def rotatedx(self, angle):
        self.image = pygame.transform.rotate(self.saved_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle -= angle

    def rotatesx(self, angle):
        self.image = pygame.transform.rotate(self.saved_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle += angle

    def creavisione(self):
        if self.direzione == 'destra':
            self.visione = pygame.Rect(
                self.ingombro.topright, self.image.get_size())
        if self.direzione == 'sinistra':
            self.visione = pygame.Rect((self.ingombro.topleft[0]-(self.image.get_size())[
                1]*2, self.ingombro.topleft[1]), self.image.get_size())
        if self.direzione == 'su':
            self.visione = pygame.Rect((self.ingombro.topleft[0], self.ingombro.topleft[1]-(
                self.image.get_size())[0]*2), self.image.get_size())
        if self.direzione == 'giù':
            self.visione = pygame.Rect(
                self.ingombro.bottomleft, self.image.get_size())

    def move(self):
        self.pos = (self.x, self.y)
        self.ingombro = pygame.Rect(self.pos, self.image.get_size())
        self.percorsoArrivo()
        if self.arrivox in range(self.x-2, self.x+2) and self.arrivoy in range(self.y-2, self.y+2):
            self.arrived = True
        if self.startpos == 'alto' and self.arrivo == 'sinistra':
            if self.y < self.arrivoy:
                self.y += self.speedy
                self.direzione = 'giù'
            if self.y in range(self.arrivoy - 2, self.arrivoy + 2) and self.angle != -95:
                self.rotatedx(5)
            if self.angle == -95:
                if self.x > self.arrivox:
                    self.x -= self.speedx
                    self.direzione = 'sinistra'
            if self.lane == 'centro':
                self.changelane()
        if self.startpos == 'alto' and self.arrivo == 'destra':
            if self.y < self.arrivoy:
                self.y += self.speedy
                self.direzione = 'giù'
            if self.y in range(self.arrivoy - 2, self.arrivoy + 2) and self.angle != 95:
                self.rotatesx(5)
            if self.angle == 95:
                if self.x < self.arrivox:
                    self.x += self.speedx
            if self.lane == 'esterna':
                self.changelanerevers()
        if self.startpos == 'basso' and self.arrivo == 'sinistra':
            if self.y > self.arrivoy:
                self.y -= self.speedy
                self.direzione = 'su'
            if self.y in range(self.arrivoy - 2, self.arrivoy + 2) and self.angle != 95:
                self.rotatesx(5)
            if self.angle == 95:
                if self.x > self.arrivox:
                    self.x -= self.speedx
                    self.direzione = 'sinistra'
            if self.lane == 'esterna':
                self.changelanerevers()
        if self.startpos == 'basso' and self.arrivo == 'destra':
            if self.y > self.arrivoy:
                self.y -= self.speedy
                self.direzione = 'su'
            if self.y in range(self.arrivoy - 2, self.arrivoy + 2) and self.angle != -95:
                self.rotatedx(5)
            if self.angle == -95:
                if self.x < self.arrivox:
                    self.x += self.speedx
                    self.direzione = 'destra'
            if self.lane == 'centro':
                self.changelane()

        if self.startpos == 'sinistra' and self.arrivo == 'alto':
            if self.x < self.arrivox:
                self.x += self.speedx
                self.direzione = 'destra'
            if self.x in range(self.arrivox-2, self.arrivox + 2) and self.angle != 95:
                self.rotatesx(5)
            if self.angle == 95:
                if self.y > self.arrivoy:
                    self.y -= self.speedy
                    self.direzione = 'su'
            if self.lane == 'esterna':
                self.changelanerevers()
        if self.startpos == 'sinistra' and self.arrivo == 'basso':
            if self.x < self.arrivox:
                self.x += self.speedx
                self.direzione = 'destra'
            if self.x in range(self.arrivox-2, self.arrivox + 2) and self.angle != -95:
                self.rotatedx(5)
            if self.angle == -95:
                if self.y < self.arrivoy:
                    self.y += self.speedy
                    self.direzione = 'giù'
            if self.lane == 'centro':
                self.changelane()
        if self.startpos == 'destra' and self.arrivo == 'alto':
            if self.x > self.arrivox:
                self.x -= self.speedx
                self.direzione = 'sinistra'
            if self.x in range(self.arrivox-2, self.arrivox + 2) and self.angle != -95:
                self.rotatedx(5)
            if self.angle == -95:
                if self.y > self.arrivoy:
                    self.y -= self.speedy
                    self.direzione = 'su'
            if self.lane == 'centro':
                self.changelane()
        if self.startpos == 'destra' and self.arrivo == 'basso':
            if self.x > self.arrivox:
                self.x -= self.speedx
                self.direzione = 'sinistra'
            if self.x in range(self.arrivox-2, self.arrivox + 2) and self.angle != 95:
                self.rotatesx(5)
            if self.angle == 95:
                if self.y < self.arrivoy:
                    self.y += self.speedy
                    self.direzione = 'giù'
            if self.lane == 'esterna':
                self.changelanerevers()
        self.creavisione()
