import pygame

# Init PyGame
pygame.init()
# costanti per schermata
sfondo = pygame.image.load('imgGame\incrocio2png.png')
sfondo = pygame.transform.scale(sfondo, (1600, 1024))
myfont = pygame.font.SysFont('Comic Sans MS', 30)
SCHERMO = pygame.display.set_mode((1600, 1024))
FPS = 60
textsurface = myfont.render('', False, (0, 0, 0))  # testo per coordinate
textsurface2 = myfont.render('', False, (0, 0, 0))  # testo per coordinate


def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
    SCHERMO.fill((0, 0, 0))


def disegna_oggetti(cars, testo1, testo2,semafori ):
    SCHERMO.blit(sfondo, (0, 0))
    SCHERMO.blit(testo1, (10, 100))
    SCHERMO.blit(testo2, (10, 10))
    for s in semafori :
        SCHERMO.blit(s.image, s.pos)
    for n in cars:
        SCHERMO.blit(n.image, n.pos)
