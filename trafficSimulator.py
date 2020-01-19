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
    n1 = Trafficlight(560, 680)
    n2 = Trafficlight(560, 107)
    n3 = Trafficlight(1100, 107)
    n4 = Trafficlight(1025, 680)
    listasemafori = [n1, n2, n3, n4]


inizializza(1)
initSemafori()
# initcordinate solo per test
x = 0
y = 0
dsds = 0
# evento per chiamare inizializza ogni tot secondi
timerlight = pygame.USEREVENT + 1
pygame.time.set_timer(timerlight, 3000)
timertrafficlight = pygame.USEREVENT + 2
pygame.time.set_timer(timertrafficlight, 9000)
spawntimer = pygame.USEREVENT + 3
pygame.time.set_timer(spawntimer, 3000)


signal_counter = 0
signal_counter1 = 1
while True:

    disegna_oggetti(listacar, textsurface, textsurface2, listasemafori)
    for i, car in enumerate(listacar):
        car.move()
        xlist = listacar.copy()
        xlist.remove(listacar[i])
        car.anticollisione(xlist)
        car.controllosemaforo(listasemafori)
        BLUE = (0, 0, 255)
        #
        #pygame.draw.rect(SCHERMO, BLUE, car.ingombro)
        # for n in listasemafori:
        #     pygame.draw.rect(SCHERMO, BLUE, n.rect)
        # pygame.draw.rect(SCHERMO, BLUE, n.rect)
        # pygame.draw.rect(SCHERMO, BLUE, car.ingombro)

        # rimuovo le auto che sono arrivate a destinazione
        if car.arrived:
            listacar.remove(car)
    time = pygame.time.get_ticks()/1000
    message = 'Time: ' + str(round(time))

    textsurface = myfont.render(message, False, (0, 0, 0))
    textsurface2 = myfont.render(
        'start'+str(listacar[0].ingombro), False, (0, 0, 0))

    aggiorna()
    for event in pygame.event.get():
        # Per ricevere coordinate sulla poszione del mouse
        # x, y = pygame.mouse.get_pos()
        # print("X : {} Y: {}".format(x, y))
        if event.type == spawntimer:
            inizializza(1)
        if event.type == timerlight:
            signal_counter1 += 1
            if signal_counter1 > 2:
                signal_counter1 = 0
        if event.type == timertrafficlight:
            signal_counter += 1
            if signal_counter > 3:
                signal_counter = 0
        listasemafori[signal_counter].change_sign(signal_counter1)
        # per inizializzare macchina con click
        if event.type == pygame.MOUSEBUTTONUP:
            inizializza(1)
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            SCHERMO = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)    
        # gestisco la chiusura della finestra
        if event.type == pygame.QUIT:
            pygame.quit()
            SystemExit
    pygame.display.flip()            
