import random
import pygame

# Coordinate
Centro = (804, 464)
EndCoordinate = [[-100, 306], [-100, 406], [940, -100], [834, -100],
                 [630, 1024], [730, 1024], [1600, 584], [1600, 490]]
LaneCoordinate = [[-100, 584], [1600, 306], [630, -100], [940, 1024]]
LaneCentrali = [[728, -100], [1600, 396], [834, 1024], [-100, 490]]


# Carico Immagini
car1img = pygame.image.load('imgGame\\auto.png')
car2img = pygame.image.load('imgGame\\auto2.png')
truckimg = pygame.image.load('imgGame\\truck.png')

auto1 = pygame.transform.scale(car1img, (68, 33))
auto2 = pygame.transform.scale(car2img, (68, 33))
truck = pygame.transform.scale(truckimg, (90, 45))
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
        if self.x == 1600:
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.x == 630 or self.x == 728:
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.x == 940 or self.x == 834:
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
        

    def checklane(self):
        if self.startpos == 'destra' or self.startpos == 'sinistra':
            if abs(self.initcoordinate[1]-Centro[1]) > 100:
                self.lane = 'esterna'
            else:
                self.lane = 'centro'
        elif self.startpos == 'alto' or self.startpos == 'basso':
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
        elif self.startpos == 'alto' or self.startpos == 'basso':
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
        elif self.startpos == 'alto' or self.startpos == 'basso':
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
            # if self.ingombro.colliderect(n.ingombro):
            #     self.arrived = True
            elif not collide:
                self.speedy = 2
                self.speedx = 2
                collide = False

    def controllosemaforo(self, listasemafori):
        #collide = False
        for s in listasemafori:
            if s.colore == 'red':
                if self.visione.colliderect(s.rect):
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
        elif self.arrivox > Centro[0] and self.arrivoy > Centro[1]:
            if self.startpos == 'sinistra':
                self.x += self.speedx
            self.arrivo = 'destra'
            self.direzione = 'destra'
        # sinistra
        elif self.arrivox < Centro[0] and self.arrivoy < Centro[1]:
            if self.startpos == 'destra':
                self.x -= self.speedx
            self.arrivo = 'sinistra'
            self.direzione = 'sinistra'

        # basso
        elif self.arrivox < Centro[0] and self.arrivoy > Centro[1]:
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
        elif self.initcoordinate[0] > Centro[0] and self.initcoordinate[1] > Centro[1]:
            self.startpos = 'basso'
        # alto
        elif self.initcoordinate[0] < Centro[0] and self.initcoordinate[1] < Centro[1]:
            self.startpos = 'alto'
        # sinistra
        elif self.initcoordinate[0] < Centro[0] and self.initcoordinate[1] > Centro[1]:
            self.startpos = 'sinistra'
        self.checklane()

    def rotatedx(self, angle):
        self.angle -= angle
        self.image = pygame.transform.rotate(self.saved_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        

    def rotatesx(self, angle):
        self.angle += angle
        self.image = pygame.transform.rotate(self.saved_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        

    def creavisione(self):

        if self.direzione == 'destra':
            card = pygame.transform.rotate(self.image, 90)
            self.visione = pygame.Rect(
                (self.ingombro.topright[0], self.ingombro.topright[1] - 14), card.get_size())
        elif self.direzione == 'sinistra':
            card = pygame.transform.rotate(self.image, 90)
            self.visione = pygame.Rect((self.ingombro.topleft[0]-(self.image.get_size())[
                1], self.ingombro.topleft[1] - 14), card.get_size())
        elif self.direzione == 'su':
            card = pygame.transform.rotate(self.image, 90)
            self.visione = pygame.Rect((self.ingombro.topleft[0] - 20, self.ingombro.topleft[1]-(
                self.image.get_size())[0]), card.get_size())
        elif self.direzione == 'giù':
            card = pygame.transform.rotate(self.image, 90)
            self.visione = pygame.Rect(
                (self.ingombro.bottomleft[0] - 20, self.ingombro.bottomleft[1]), card.get_size())
        # prima versione
        # if self.direzione == 'destra':
        #     self.visione = pygame.Rect(
        #         self.ingombro.topright, self.image.get_size())
        # if self.direzione == 'sinistra':
        #     self.visione = pygame.Rect((self.ingombro.topleft[0]-(self.image.get_size())[
        #         1]*2, self.ingombro.topleft[1]), self.image.get_size())
        # if self.direzione == 'su':
        #     self.visione = pygame.Rect((self.ingombro.topleft[0], self.ingombro.topleft[1]-(
        #         self.image.get_size())[0]*2), self.image.get_size())
        # if self.direzione == 'giù':
        #     self.visione = pygame.Rect(
        #         self.ingombro.bottomleft, self.image.get_size())

    def move(self):
        self.pos = (self.x, self.y)
        self.ingombro = pygame.Rect(self.pos, self.image.get_size())
        self.percorsoArrivo()
        if self.x in range(self.arrivox - 2, self.arrivox +2) and self.y in range(self.arrivoy - 2, self.arrivoy + 2):
            self.arrived = True
        elif self.x < - 100 or self.x > 1600 or self.y < -100 or self.y > 1024:
            self.arrived = True     
        else:
            if self.startpos == 'alto' and self.arrivo == 'sinistra':
                if self.y < self.arrivoy:
                    self.y += self.speedy
                    self.direzione = 'giù'
                elif self.y in range(self.arrivoy - 2, self.arrivoy + 2) and self.angle != -90:
                    self.rotatedx(5)
                elif self.angle == -90:
                    if self.x > self.arrivox:
                        self.x -= self.speedx
                        self.direzione = 'sinistra'
                if self.lane == 'centro':
                    self.changelane()
            if self.startpos == 'alto' and self.arrivo == 'destra':
                if self.y < self.arrivoy:
                    self.y += self.speedy
                    self.direzione = 'giù'
                elif self.y in range(self.arrivoy - 2, self.arrivoy + 2) and self.angle != 90:
                    self.rotatesx(5)
                elif self.angle == 90:
                    if self.x < self.arrivox:
                        self.x += self.speedx
                if self.lane == 'esterna':
                    self.changelanerevers()
            if self.startpos == 'basso' and self.arrivo == 'sinistra':
                if self.y > self.arrivoy:
                    self.y -= self.speedy
                    self.direzione = 'su'
                elif self.y in range(self.arrivoy - 2, self.arrivoy + 2) and self.angle != 90:
                    self.rotatesx(5)
                elif self.angle == 90:
                    if self.x > self.arrivox:
                        self.x -= self.speedx
                        self.direzione = 'sinistra'
                if self.lane == 'esterna':
                    self.changelanerevers()
            if self.startpos == 'basso' and self.arrivo == 'destra':
                if self.y > self.arrivoy:
                    self.y -= self.speedy
                    self.direzione = 'su'
                elif self.y in range(self.arrivoy - 2, self.arrivoy + 2) and self.angle != -90:
                    self.rotatedx(5)
                elif self.angle == -90:
                    if self.x < self.arrivox:
                        self.x += self.speedx
                        self.direzione = 'destra'
                if self.lane == 'centro':
                    self.changelane()

            if self.startpos == 'sinistra' and self.arrivo == 'alto':
                if self.x < self.arrivox:
                    self.x += self.speedx
                    self.direzione = 'destra'
                elif self.x in range(self.arrivox-2, self.arrivox + 2) and self.angle != 90:
                    self.rotatesx(5)
                elif self.angle == 90:
                    if self.y > self.arrivoy:
                        self.y -= self.speedy
                        self.direzione = 'su'
                if self.lane == 'esterna':
                    self.changelanerevers()
            if self.startpos == 'sinistra' and self.arrivo == 'basso':
                if self.x < self.arrivox:
                    self.x += self.speedx
                    self.direzione = 'destra'
                elif self.x in range(self.arrivox-2, self.arrivox + 2) and self.angle != -90:
                    self.rotatedx(5)
                elif self.angle == -90:
                    if self.y < self.arrivoy:
                        self.y += self.speedy
                        self.direzione = 'giù'
                if self.lane == 'centro':
                    self.changelane()
            if self.startpos == 'destra' and self.arrivo == 'alto':
                if self.x > self.arrivox:
                    self.x -= self.speedx
                    self.direzione = 'sinistra'
                elif self.x in range(self.arrivox-2, self.arrivox + 2) and self.angle != -90:
                    self.rotatedx(5)
                elif self.angle == -90:
                    if self.y > self.arrivoy:
                        self.y -= self.speedy
                        self.direzione = 'su'
                if self.lane == 'centro':
                    self.changelane()
            if self.startpos == 'destra' and self.arrivo == 'basso':
                if self.x > self.arrivox:
                    self.x -= self.speedx
                    self.direzione = 'sinistra'
                elif self.x in range(self.arrivox-2, self.arrivox + 2) and self.angle != 90:
                    self.rotatesx(5)
                elif self.angle == 90:
                    if self.y < self.arrivoy:
                        self.y += self.speedy
                        self.direzione = 'giù'
                if self.lane == 'esterna':
                    self.changelanerevers()
            self.creavisione()
