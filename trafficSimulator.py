# Importo librerie
import pygame
import datetime
import random
from grafica import *
from veicolo import *
from trafficlight import *


# Costanti Globale
listacar = list()


def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    if hour == 24:
        hour = 0
    #return "%02d:%02d" % (hour, min)
    return (hour, min)


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
def trafficSet(timesimulator):
    ora = int(convert(timesimulator)[0])
    if ora < 8 or ora > 21:
        return 1
    elif ora in range(8,11) or ora in range(14,18):
        return 2
    else:
        return 3        



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
pygame.time.set_timer(pygame.USEREVENT+4, 1)


signal_counter = 0
signal_counter1 = 1
s1 = 0
# prima prova per regolare spawn macchine su ora
newCar = 1
while True:
    newCar = trafficSet(s1*30)
    disegna_oggetti(listacar, textsurface, textsurface2, listasemafori)
    for i, car in enumerate(listacar):
        car.move()
        xlist = listacar.copy()
        xlist.remove(listacar[i])
        car.anticollisione(xlist)
        car.controllosemaforo(listasemafori)
        BLUE = (0, 0, 255)
        #
        # pygame.draw.rect(SCHERMO, BLUE, car.visione)
        # for n in listasemafori:
        #     pygame.draw.rect(SCHERMO, BLUE, n.rect)
        # pygame.draw.rect(SCHERMO, BLUE, n.rect)
        # pygame.draw.rect(SCHERMO, BLUE, car.ingombro)

        # rimuovo le auto che sono arrivate a destinazione
        if car.arrived:
            listacar.remove(car)
    # s = round(pygame.time.get_ticks(),2)

    textsurface = myfont.render(
        'Numero veicoli:  ' + str(len(listacar)), False, (0, 0, 0))
    textsurface2 = myfont.render(
        'Time:  ' + "%02d:%02d" % convert(s1*30), False, (0, 0, 0))
    # textsurface2 = myfont.render(
    #     'start'+str(listacar[0].ingombro), False, (0, 0, 0))

    for event in pygame.event.get():
        # Per ricevere coordinate sulla poszione del mouse
        # x, y = pygame.mouse.get_pos()
        # print("X : {} Y: {}".format(x, y))
        if event.type == spawntimer:
            inizializza(newCar)
        if event.type == pygame.USEREVENT+4:
            s1 += 1
            if s1 == 2880:
                s1 = 0
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
    aggiorna()
    pygame.display.flip()
