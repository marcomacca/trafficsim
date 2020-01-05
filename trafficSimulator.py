# Importo librerie
import pygame,random
from grafica import *
from veicolo import *


# Costanti Globale


listacar = list()


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

    disegna_oggetti(listacar, textsurface, textsurface2)
    for car in listacar:
        car.move()
        car.ingombro = pygame.Rect(car.x, car.y, car.rect[2], car.rect[3])
        # rimuovo le auto che sono arrivate a destinazione
        if car.arrived:
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
        # gestisco la chiusura della finestra    
        if event.type == pygame.QUIT:  
            pygame.quit()
            SystemExit
