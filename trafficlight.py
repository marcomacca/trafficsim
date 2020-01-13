import pygame
signal_list = ['imgGame\\green.png', 'imgGame\\yellow.png', 'imgGame\\red.png']

# n2 = Trafficlight(560,107)
# n3 = Trafficlight(1100,107)
# n4 = Trafficlight(1025,680)


class Trafficlight():
    def __init__(self, x, y):
        self.image = pygame.image.load('imgGame\\green.png')
        self.image = pygame.transform.scale(self.image, (31, 81))
        self.pos = (x, y)
        self.rect = None
        self.createrect()
        self.colore = 'green'
        # self.rect=self.image.get_rect(center=(700,50))

    def change_sign(self, index):
        color = signal_list[index]
        self.image = pygame.image.load(color)
        self.image = pygame.transform.scale(self.image, (31, 81))
        if index == 0:
            self.colore = 'green'
        elif index == 1:
            self.colore = 'orange'
        elif index == 2:
            self.colore = 'red'        
        

    def createrect(self):
        if self.pos[0] == 560 and self.pos[1] == 680:
            self.rect = pygame.Rect((496, 471), (20, 180))
        elif self.pos[0] == 560 and self.pos[1] == 107:
            self.rect = pygame.Rect((592, 188), (200, 20))
        elif self.pos[0] == 1100 and self.pos[1] == 107:
            self.rect = pygame.Rect((1090, 282), (20, 180))
        elif self.pos[0] == 1025 and self.pos[1] == 680:
            self.rect = pygame.Rect((810, 720), (200, 20))
