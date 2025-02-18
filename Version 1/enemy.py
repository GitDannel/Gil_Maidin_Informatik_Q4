#enemy.py
import pygame
import random
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png") #Lädt das Gegnerbild
        self.rect = self.image.get_rect(topleft=(random.randint(0, WIDTH-40), random.randint(0, HEIGHT-40))) #Macht zufällige Startposition
        self.health = 30 #Gibt Lebenspunkte der Gegner an
    
    def update(self):
        pass #Gegnerbewegung können wir hier
