import pygame
import random
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png") #Lädt das Gegnerbild
        self.rect = self.image.get_rect(topleft=(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))) #Macht zufällige Startposition
        self.health = 30 #Gibt Lebenspunkte der Gegner an
    
    def update(self):
        pass #Gegnerbewegung können wir hier