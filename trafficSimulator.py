# Importo librerie
import pygame
import random
from grafica import *

from collisioncontroller import *
from veicolo import *
from trafficlight import *


# Costanti Globale
listacar = list()


def inizializza(Numerocars):
    global listacar
    for n in range(Numerocars):
        a = Car()
        listacar.append(a)


inizializza(10)
# initcordinate solo per test
x = 0
y = 0
dsds = 0

while True:
    b = Trafficlight()
    disegna_oggetti(listacar, textsurface, textsurface2, b)
    for car in listacar:
        car.move()
        BLUE = (0, 0, 255)
        #pygame.draw.rect(SCHERMO, BLUE, car.visione)
        # pygame.draw.rect(SCHERMO, BLUE, car.ingombro)
       

        # rimuovo le auto che sono arrivate a destinazione
        if car.arrived:
            listacar.remove(car)
    textsurface2 = myfont.render(
        'start'+str(listacar[0].ingombro), False, (0, 0, 0))
    textsurface = myfont.render(
        'collisioni'+str(listacar[0].direzione), False, (0, 0, 0))
    checkCollision(listacar)
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
