#Größte Änderungen zu letzter Version:
#in update zurückattacken
#Bilder gescaled auf eine Größe
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
        attack_range = 40 #Gegner kann nur schlagen wenn Spieler nahe ist
        if abs(self.rect.centerx - player.rect.centerx) <= attack_range and abs(self.rect.centery - player.rect.centery) <= attack_range: #Hier wird die horizontale Entfernung zwischen Spieler & Gegner berechnet.
                #Falls die Entfernung kleiner als attack_range ist, kann der Angriff treffen. # abs() basically Betragsstriche
            player.health -= 5 #Gegner verursacht Schaden am Spieler

        #Gegnerbewegung können wir hier