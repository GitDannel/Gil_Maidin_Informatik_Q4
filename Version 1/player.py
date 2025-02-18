#player.py
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png") #Lädt das Spielerbild
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2)) #Macht die Startposition
        self.speed = 5 #Gibt die Bewegungsgeschwindigkeit an
        self.health = 100 #Gibt die Lebenspunkte an

    def handle_event(self, event):
        pass #Hier könnte auch Tastatureingabe geaddet werden

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed #Bewegt Spieler nach links
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed #Bewegt Spieler nach rechts
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed #Bewegt Spieler nach oben
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed #Bewegt Spieler nach unten

    def draw(self, surface):
        surface.blit(self.image, self.rect) #Zeichnet das Spielerbild auf den Bildschirm (Position siehe oben self.rect)