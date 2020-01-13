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
def initSemafori():
    global listasemafori
    n1 = Trafficlight(329,596)
    n2 = Trafficlight(329,107)
    n3 = Trafficlight(680,107)
    n4 = Trafficlight(680,595)
    listasemafori = [n1,n2,n3,n4]
    



inizializza(1)
initSemafori()
# initcordinate solo per test
x = 0
y = 0
dsds = 0
#evento per chiamare inizializza ogni secondo
TIMER1_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER1_EVENT, 2000)

signal_counter = 0
while True:
    
    disegna_oggetti(listacar, textsurface, textsurface2,listasemafori)
    for i,car in enumerate(listacar):
        car.move()
        xlist = listacar.copy()
        xlist.remove(listacar[i])
        car.provacollisione(xlist)
        BLUE = (0, 0, 255)
        #pygame.draw.rect(SCHERMO, BLUE, car.visione)
        # pygame.draw.rect(SCHERMO, BLUE, car.ingombro)
       

        # rimuovo le auto che sono arrivate a destinazione
        if car.arrived:
            listacar.remove(car)
    time = pygame.time.get_ticks()/1000
    message = 'Time: ' + str(round(time))

    textsurface = myfont.render(message, False, (0, 0, 0))       
    textsurface2 = myfont.render(
        'start'+str(listacar[0].ingombro), False, (0, 0, 0))
    # textsurface = myfont.render(
    #     'collisioni'+str(listacar[0].direzione), False, (0, 0, 0))
    
    aggiorna()
    for event in pygame.event.get():
        # Per ricevere coordinate sulla poszione del mouse
        x, y = pygame.mouse.get_pos()
        print("X : {} Y: {}".format(x, y))
        if event.type == TIMER1_EVENT:
            inizializza(1)
        # per inizializzare macchina con click
        if event.type == pygame.MOUSEBUTTONUP:
            signal_counter+=1
            if signal_counter>2:
                signal_counter=0 
            for n in listasemafori:
                n.change_sign(signal_counter)

            # inizializza(1)
            # print("click")
        # gestisco la chiusura della finestra
        if event.type == pygame.QUIT:
            pygame.quit()
            SystemExit
