#Größte Änderungen zu letzter Version:
#handle_event methode damit mit keybind statt Kollision dmgen kann
#attack methode
#Bilder gescaled auf eine Größe
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png") #Lädt das Spielerbild
        self.image = pygame.transform.scale(self.image, (50, 50)) #Skaliert das Bild auf 50x50 Pixel
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 100)) #Macht die Startposition
        self.speed = 5 #Bewegungsgeschwindigkeit
        self.health = 100 #Lebenspunkte
    
    def handle_event(self, event, enemies):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: #Taste "1" für Angriff
                self.attack(enemies)
        #Hier könnten wir auch andere Tastatureingaben adden

    def attack(self, enemies):
        attack_range = 100  #Angriff ist möglich wenn Gegner in 50px Entfernung ist
        for enemy in enemies: #for enemy in pygame.sprite.spritecollide(self, enemies, False):
            if abs(self.rect.centerx - enemy.rect.centerx) <= attack_range and abs(self.rect.centery - enemy.rect.centery) <= attack_range: #Hier wird die horizontale Entfernung zwischen Spieler & Gegner berechnet.
                    #Falls die Entfernung kleiner als attack_range ist, kann der Angriff treffen. # abs() basically Betragsstriche
                enemy.health -= 10 #Gegner verliert HP
                print("Gegner getroffen! HP: " + str(enemy.health)) #Test-Ausgabe, ob alles klappt soweit
                if enemy.health <= 0:
                    enemies.remove(enemy) #Entferne den Gegner, wenn er 0 HP hat
    
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
        if any(self.rect.colliderect(enemy.rect) for enemy in enemies):
            self.rect.x -= move_x  #Rückgängigmachen falls Kollision damit nicht ineinander laufen
        
        self.rect.y += move_y
        if any(self.rect.colliderect(enemy.rect) for enemy in enemies):
            self.rect.y -= move_y  #Rückgängigmachen falls Kollision damit nicht ineinander laufen
    
    def reset_position(self):
        self.rect.center = (WIDTH//2, HEIGHT - 100) #Setzt den Spieler zurück zur Startposition
    
    def draw(self, screen):
        screen.blit(self.image, self.rect) #Zeichnet das Spielerbild auf den Bildschirm (Position siehe oben self.rect)

