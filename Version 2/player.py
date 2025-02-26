#Größte Änderungen zu letzter Version:
#reset_position Methode für leichter
#Kollisionen nicht mehr möglich
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png") #Lädt das Spielerbild
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 100)) #Macht die Startposition
        self.speed = 5 #Bewegungsgeschwindigkeit
        self.health = 100 #Lebenspunkte
    
    def handle_event(self, event):
        pass #Hier könnte auch Tastatureingabe geaddet werden
    
    #Also im Prinzip man drückt ne Taste dann wird ja geupdated dann move_x und y wieder = 0 und je nachdem was gedrückt wird move_x und y dann mit dem pos. oder neg. speed wert belegt und unten rect dann bewegt
    def update(self, enemies):
        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0
        if keys[pygame.K_LEFT]:
            move_x = -self.speed #Bewegt Spieler nach links
        if keys[pygame.K_RIGHT]:
            move_x = self.speed #Bewegt Spieler nach rechts
        if keys[pygame.K_UP]:
            move_y = -self.speed #Bewegt Spieler nach oben
        if keys[pygame.K_DOWN]:
            move_y = self.speed #Bewegt Spieler nach unten
        
        #statt:
        # if keys[pygame.K_LEFT]:
        #     self.rect.x -= self.speed
        # if keys[pygame.K_RIGHT]:
        #     self.rect.x += self.speed
        # if keys[pygame.K_UP]:
        #     self.rect.y -= self.speed
        # if keys[pygame.K_DOWN]:
        #     self.rect.y += self.speed
        
        self.rect.x += move_x
        if any(self.rect.colliderect(enemy.rect) for enemy in enemies):
            self.rect.x -= move_x #Rückgängigmachen falls Kollision damit nicht ineinander laufen
        
        self.rect.y += move_y
        if any(self.rect.colliderect(enemy.rect) for enemy in enemies):
            self.rect.y -= move_y #Rückgängigmachen falls Kollision damit nicht ineinander laufen

    def reset_position(self):
        self.rect.center = (WIDTH//2, HEIGHT - 100) #Setzt den Spieler zurück zur Startposition

    def draw(self, screen):
        screen.blit(self.image, self.rect) #Zeichnet das Spielerbild auf den Bildschirm (Position siehe oben self.rect)

