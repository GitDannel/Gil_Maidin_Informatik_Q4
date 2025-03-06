#Größte Änderungen zu letzter Version:
#Tilesize für Cluster für später leichter Map und Wände
#damage jetzt in self.damage um später leichter anpassen zu können
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png") #Lädt das Spielerbild
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE)) #Skaliert das Bild auf 50x50 Pixel also ein TILESIZE
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - TILESIZE)) #Macht die Startposition
        self.speed = TILESIZE // 10  #Bewegungsgeschwindigkeit ist eine Tile-Größe durch 10
        self.max_health = 100
        self.health = 100 #Lebenspunkte
        self.damage = 10
    
    def handle_event(self, event, enemies):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: #Taste "1" für Angriff
                self.attack(enemies)
        #Hier könnten wir auch andere Tastatureingaben adden
    
    def attack(self, enemies):
        attack_range_x = TILESIZE * 1.5  #50% Größere horizontale Reichweite
        attack_range_y = TILESIZE * 1.5  #50% Größere vertikale Reichweite
        for enemy in enemies:
            if abs(self.rect.centerx - enemy.rect.centerx) <= attack_range_x and abs(self.rect.centery - enemy.rect.centery) <= attack_range_y: #Hier wird die horizontale Entfernung zwischen Spieler & Gegner berechnet.
                    #Falls die Entfernung kleiner als attack_range ist, kann der Angriff treffen. # abs() basically Betragsstriche
                enemy.take_damage(self.damage) #Gegner verliert HP
                print("Gegner getroffen! HP: " + str(enemy.health)) #Test-Ausgabe, ob alles klappt soweit
                if enemy.health <= 0:
                    enemies.remove(enemy) #Entferne den Gegner, wenn er 0 HP hat
                    self.health = self.max_health
    
    def update(self, enemies):
        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0
        if keys[pygame.K_LEFT]:
            move_x = -self.speed #Bewegt den Spieler nach links
        if keys[pygame.K_RIGHT]:
            move_x = self.speed #Bewegt den Spieler nach rechts
        if keys[pygame.K_UP]:
            move_y = -self.speed #Bewegt den Spieler nach oben
        if keys[pygame.K_DOWN]:
            move_y = self.speed #Bewegt den Spieler nach unten

        self.rect.x += move_x
        if any(self.rect.colliderect(enemy.rect) for enemy in enemies): #Geht auch while statt if, weil jetzt nicht wenn Kollision erkannt zurückgemacht wird sondern solange bis keine Kollision mehr (Können jetzt pixelperfect angrenzen)
            self.rect.x -= move_x  #Rückgängigmachen falls Kollision damit nicht ineinander laufen
        
        self.rect.y += move_y
        if any(self.rect.colliderect(enemy.rect) for enemy in enemies):
            self.rect.y -= move_y  #Rückgängigmachen falls Kollision damit nicht ineinander laufen
    
    def reset_position(self):
        self.rect.center = (WIDTH//2, HEIGHT - TILESIZE) #Setzt den Spieler zurück zur Startposition
    
    def draw(self, screen):
        screen.blit(self.image, self.rect) #Zeichnet das Spielerbild auf den Bildschirm (Position siehe oben self.rect)
        
        
    