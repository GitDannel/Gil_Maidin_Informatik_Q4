#game.py
import pygame
from player import Player
from enemy import Enemy
from settings import *
# import random

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Erstellt das Spielfenster
        pygame.display.set_caption("Dungeon Game") #Gibt den Fenstertitel an
        self.clock = pygame.time.Clock() #Erstellt eine clock für die Framerate
        self.running = True #Variable für die Spielschleife
        self.background = pygame.image.load("background.jpg") #Lädt das Hintergrundbild
        self.player = Player() #Erstellt den Spieler
        self.enemies = pygame.sprite.Group(Enemy() for _ in range(3)) #Erstellt eine Gruppe von Gegnern
        self.portal = pygame.Rect(WIDTH - 60, HEIGHT // 2, 50, 50) #Erstellt das Portal
    
    def run(self):
        while self.running:
            self.handle_events() #Verarbeitet Benutzer-Eingaben
            self.update() #Aktualisiert das Spielgeschehen
            self.draw() #Zeichnet also quasi setzt die Elemente auf den Bildschirm
        pygame.quit() #Beendet Pygame wenn die Schleife stoppt

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False #Schließt das Spiel wenn das Fenster geschlossen wird
            self.player.handle_event(event) #Übergibt Ereignisse an den Spieler
    
    def update(self):
        self.player.update() #Aktualisiert die Position des Spielers
        self.enemies.update() #Aktualisiert alle Gegner
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect): #Prüft auf Kollision mit Gegner
                self.player.health -= 1 #Verringert Spieler HP
                enemy.health -= 10 #Gegner verliert Leben
                if enemy.health <= 0:
                    self.enemies.remove(enemy) #Entfernt besiegte Gegner
                if self.player.health <= 0:
                    self.running = False #Beendet das Spiel, wenn die HP auf 0 fallen
        
        if not self.enemies: #Prüft, ob alle Gegner besiegt sind
            if self.player.rect.colliderect(self.portal): #Prüft, ob der Spieler das Portal erreicht
                self.enemies = pygame.sprite.Group(Enemy() for _ in range(3)) #Erstellt neue Gegner für das nächste Level
    
    def draw(self):
        self.screen.blit(self.background, (0, 0)) #Zeichnet den Hintergrund
        self.player.draw(self.screen) #Zeichnet den Spieler
        self.enemies.draw(self.screen) #Zeichnet alle Gegner
        pygame.draw.rect(self.screen, (255, 255, 0), self.portal) #Zeichnet das Portal
        self.draw_health() #Zeichnet die HP-Anzeige
        pygame.display.flip() #Aktualisiert das Fenster
        self.clock.tick(FPS) #Setzt die Bildrate
    
    def draw_health(self):
        font = pygame.font.Font(None, 30)
        health_text = font.render("Health: " + str(self.player.health), True, (255, 255, 255)) #oder als f-string
        self.screen.blit(health_text, (10, HEIGHT - 30)) #Zeigt die Spieler-HP unten an