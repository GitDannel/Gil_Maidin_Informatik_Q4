#Größte Änderungen zu letzter Version:
#Tilesize für Cluster für später leichter Map und Wände
#draw_health für Leben der gegner über denen
#take_damage um damage zu speichern für draw_damage also dass der damage angezeigt werden kann
#damage jetzt in self.damage um später leichter anpassen zu können
import pygame
import random
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png") #Lädt das Gegnerbild
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE)) #Skaliert das Bild auf 50x50 Pixel
        self.rect = self.image.get_rect(topleft=(random.randint(2, (WIDTH // TILESIZE) - 2) * TILESIZE, random.randint(2, (HEIGHT // TILESIZE) - 2) * TILESIZE)) #Macht zufällige Startposition
        self.health = 30 #Gibt Lebenspunkte der Gegner an
        self.damage_display_time = 0 #Timer für Damage-Anzeige
        self.last_damage = 0 #Zuletzt erhaltener dmg
        self.last_attack_time = 0 #Timer (speichert wann zuletzt angegriffen wurde)
        self.attack_delay = 500 #500 Millisekunden (0,5 Sekunden Wartezeit zwischen Angriffen)
        self.damage = 5

    def update(self, player, screen):
        self.attack(player) #Führt den Angriff mit Delay aus
        self.draw_health(screen)
        self.draw_damage(screen)
        #Gegnerbewegung können wir hier
    
    def attack(self, player):
        now = pygame.time.get_ticks() #Aktuelle Zeit in Millisekunden holen
        if now - self.last_attack_time > self.attack_delay: #Prüfen ob genug Zeit vergangen ist
            attack_range_x = TILESIZE * 1.5  # Größere horizontale Reichweite
            attack_range_y = TILESIZE * 1.5  # Größere vertikale Reichweite
            if abs(self.rect.centerx - player.rect.centerx) <= attack_range_x and abs(self.rect.centery - player.rect.centery) <= attack_range_y: #Hier wird die horizontale Entfernung zwischen Spieler & Gegner berechnet.
                #Falls die Entfernung kleiner als attack_range ist, kann der Angriff treffen. # abs() basically Betragsstriche
                player.health -= self.damage #Gegner verursacht Schaden am Spieler
                self.last_attack_time = now #Aktualisiert die letzte Angriffszeit
                #statt time.sleep weil ganzes Spiel irgendwie verlangsamt

    def take_damage(self, amount):
        self.health -= amount
        self.last_damage = amount
        self.damage_display_time = pygame.time.get_ticks()

    def draw_health(self, screen):
        self.font = pygame.font.Font(None, 30)
        hp_text = self.font.render(str(self.health), True, (255, 0, 0))
        screen.blit(hp_text, (self.rect.centerx - 10, self.rect.top - 20))
    
    def draw_damage(self, screen):
        self.font = pygame.font.Font(None, 30)
        if pygame.time.get_ticks() - self.damage_display_time < 125:
            dmg_text = self.font.render(str(self.last_damage), True, (255, 0, 0))
            screen.blit(dmg_text, (self.rect.centerx + 15, self.rect.top - 20))
            

                


