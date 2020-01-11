import pygame
signal_list = ['imgGame\\green.png', 'imgGame\\yellow.png', 'imgGame\\red.png']


class Trafficlight():
    def __init__(self):
        self.image = pygame.image.load('imgGame\\green.png')
        self.image = pygame.transform.scale(self.image, (31, 81))
        # self.rect=self.image.get_rect(center=(700,50))

    def change_sign(self, color):
        self.image = pygame.image.load(color)
        self.image = pygame.transform.scale(self.image, (31,81))
