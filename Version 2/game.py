#Größte Änderungen zu letzter Version:
#Portal entsteht jetzt erst an random Ort wenn alle Gegner tot sind
#spawn_enemies Methode damit einfacher und dass Gegner nicht mehr im Spieler
import pygame
from player import Player
from enemy import Enemy
from settings import *
import random

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Erstellt das Spielfenster
        pygame.display.set_caption("Dungeon Game") #Gibt den Fenstertitel an
        self.clock = pygame.time.Clock() #Erstellt eine clock für die Framerate
        self.running = True #Variable für die Spielschleife
        self.background = pygame.image.load("background.jpg") #Lädt das Hintergrundbild
        self.player = Player() #Erstellt den Spieler
        self.enemies = pygame.sprite.Group() #Erstellt eine leere Gegner Gruppe
        self.portal = None #Portal wird erst erstellt wenn alle Gegner besiegt sind
        self.spawn_enemies() #Erstellt die Gegner beim Spielstart
    
    def spawn_enemies(self):
        while len(self.enemies) < 3: #Bis 3 Gegner spawnen Gegner also das hier damit 3 Gegner spawnen
            enemy = Enemy()
            #dass Gegner nicht mehr im Portal oder direkt beim Spieler spawnen
            if not enemy.rect.colliderect(self.player.rect): #Wenn erzeugter Gegner nicht kollidiert mit Spieler Rechteck
                self.enemies.add(enemy) #dann wird Gruppe hinzugefügt
    
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
        self.player.update(self.enemies) #Aktualisiert die Position des Spielers
        self.enemies.update() #Aktualisiert alle Gegner(dmg)
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect): #Prüft auf Kollision mit Gegner
                self.player.health -= 1 #Verringert Spieler HP
                enemy.health -= 10 #Gegner verliert Leben
                if enemy.health <= 0:
                    self.enemies.remove(enemy) #Entfernt besiegte Gegner
                if self.player.health <= 0:
                    self.running = False #Beendet das Spiel, wenn die HP auf 0 fallen
        
        if not self.enemies and self.portal is None: #Wenn alle Gegner tot sind Portal erzeugen
            self.portal = pygame.Rect(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), 50, 50) #Erstellt das Portal an zufälligem Ort in grenzen

        if self.portal and self.player.rect.colliderect(self.portal): #Wenn Portal da und Spieler Rechteck berührt
            self.portal = None #Entfernt das alte Portal wieder
            self.spawn_enemies() #Erstellt neue Gegner für das nächste Level
            self.player.reset_position() #Setzt den Spieler zurück zum Startpunkt
    
    def draw(self):
        self.screen.blit(self.background, (0, 0)) #Zeichnet den Hintergrund
        self.player.draw(self.screen) #Zeichnet den Spieler
        self.enemies.draw(self.screen) #Zeichnet alle Gegner
        if self.portal:
            pygame.draw.rect(self.screen, (255, 255, 0), self.portal)  #Zeichnet das Portal falls vorhanden
        self.draw_health() #Zeichnet die HP-Anzeige
        pygame.display.flip() #Aktualisiert das Fenster
        self.clock.tick(FPS) #Setzt die Bildrate
    
    def draw_health(self):
        font = pygame.font.Font(None, 30)
        health_text = font.render("Health: " + str(self.player.health), True, (255, 255, 255)) #oder als f-string
        self.screen.blit(health_text, (10, HEIGHT - 30))  #Zeigt die Spieler-HP unten an