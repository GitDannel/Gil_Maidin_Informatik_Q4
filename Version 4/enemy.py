#Größte Änderungen zu letzter Version:
#Angriffsreichweite an Bildgröße angepasst statt flat wert damit das bei allen Bildgrößen klappt
#kleinere dmg ticks
import pygame
import random
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png") #Lädt das Gegnerbild
        self.image = pygame.transform.scale(self.image, (50, 50)) #Skaliert das Bild auf 50x50 Pixel
        self.rect = self.image.get_rect(topleft=(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))) #Macht zufällige Startposition
        self.health = 30 #Gibt Lebenspunkte der Gegner an
    
    def update(self, player):
        attack_range = max(self.image.get_width(), self.image.get_height()) + 10 #Angriffsreichweite basierend auf Bildgröße #max nimmt größten Wert von beiden
        if abs(self.rect.centerx - player.rect.centerx) <= attack_range and abs(self.rect.centery - player.rect.centery) <= attack_range: #Hier wird die horizontale Entfernung zwischen Spieler & Gegner berechnet.
                #Falls die Entfernung kleiner als attack_range ist, kann der Angriff treffen. # abs() basically Betragsstriche
            player.health -= 1 #Gegner verursacht Schaden am Spieler

        #Gegnerbewegung können wir hier