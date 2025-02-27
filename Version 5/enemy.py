#Größte Änderungen zu letzter Version:
#Unterschieden in horizontale und vertikale Reichweite als fix für hochkante Bilder
#neue Bilder
#attack methode damit man die ticks besser dafür bestimmen kann
import pygame
import random
from settings import *
import time

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png") #Lädt das Gegnerbild
        self.image = pygame.transform.scale(self.image, (50, 50)) #Skaliert das Bild auf 50x50 Pixel
        self.rect = self.image.get_rect(topleft=(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))) #Macht zufällige Startposition
        self.health = 30 #Gibt Lebenspunkte der Gegner an
        self.last_attack_time = 0 #Timer (speichert wann zuletzt angegriffen wurde)
        self.attack_delay = 100 #100 Millisekunden (0,1 Sekunden Wartezeit zwischen Angriffen)

    def update(self, player):
        self.attack(player) #Führt den Angriff mit Delay aus
        #Gegnerbewegung können wir hier

    def attack(self, player):
        now = pygame.time.get_ticks() #Aktuelle Zeit in Millisekunden holen
        if now - self.last_attack_time > self.attack_delay: #Prüfen ob genug Zeit vergangen ist
            attack_range_x = self.image.get_width() + 10
            attack_range_y = self.image.get_height() + 10
            if abs(self.rect.centerx - player.rect.centerx) <= attack_range_x and abs(self.rect.centery - player.rect.centery) <= attack_range_y: #Hier wird die horizontale Entfernung zwischen Spieler & Gegner berechnet.
                #Falls die Entfernung kleiner als attack_range ist, kann der Angriff treffen. # abs() basically Betragsstriche
                player.health -= 1 #Gegner verursacht Schaden am Spieler
                self.last_attack_time = now #Aktualisiert die letzte Angriffszeit
                #statt time.sleep weil ganzes Spiel irgendwie verlangsamt:
    
    