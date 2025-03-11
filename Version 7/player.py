#Größte Änderungen zu letzter Version:
#self.level, xp, xp_to_next_level um level aufsteigen zu können durch gain_xp und level_up Methoden und Gegnern, die jetzt xp geben
#kill gibt keine full hp mehr
import pygame
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png") #Lädt das Spielerbild
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE)) #Skaliert das Bild auf 50x50 Pixel also ein TILESIZE
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - TILESIZE)) #Macht die Startposition
        self.level = 1
        self.xp = 0
        self.xp_for_next_level = 100
        self.speed = TILESIZE // 10  #Bewegungsgeschwindigkeit ist eine Tile-Größe durch 10
        self.max_health = 100
        self.health = 100 #Lebenspunkte
        self.attack_damage = 10
        self.attack_range_x = TILESIZE * 1.5  #50% Größere horizontale Reichweite
        self.attack_range_y = TILESIZE * 1.5  #50% Größere vertikale Reichweite
    
    def handle_event(self, event, enemies):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: #Taste "1" für Angriff
                self.attack(enemies)
        #Hier könnten wir auch andere Tastatureingaben adden
    
    def attack(self, enemies):
        for enemy in enemies:
            if abs(self.rect.centerx - enemy.rect.centerx) <= self.attack_range_x and abs(self.rect.centery - enemy.rect.centery) <= self.attack_range_y: #Hier wird die horizontale Entfernung zwischen Spieler & Gegner berechnet.
                    #Falls die Entfernung kleiner als attack_range ist, kann der Angriff treffen. # abs() basically Betragsstriche
                enemy.take_damage(self.attack_damage) #Gegner verliert HP
                print("Gegner getroffen! HP: " + str(enemy.health)) #Test-Ausgabe, ob alles klappt soweit
                if enemy.health <= 0:
                    enemies.remove(enemy) #Entferne den Gegner, wenn er 0 HP hat
                    self.gain_xp(random.randint(10,20)) #self.gain_xp(enemy.health * 2)  # XP basiert auf HP des Gegners
    
    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_for_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.xp_for_next_level *= 1.5  #XP benötigt steigt
        self.max_health += 10
        self.health = self.max_health #oder +=10 einfach wenn man nicht zu viel full hp geben will je nachdem ob noch tränke
        self.attack_damage += 2
        self.speed += 1
        print("Level Up! Neues Level: " + str(self.level))
    
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
        
        
    