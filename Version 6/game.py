#Größte Änderungen zu letzter Version:
#Tilesize für Cluster für später leichter Map und Wände
#Gegner HP über ihnen angezeigt und auch Schaden den sie bekommen
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
        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, (TILESIZE * (WIDTH // TILESIZE), TILESIZE * (HEIGHT // TILESIZE))) #Passt den Hintergrund an die Tile Größe an
        self.player = Player() #Erstellt den Spieler
        self.enemies = pygame.sprite.Group() #Erstellt eine leere Gegner Gruppe
        self.portal = None  #Portal wird erst erstellt wenn alle Gegner besiegt sind
        self.spawn_enemies() #Erstellt die Gegner beim Spielstart
    
    def spawn_enemies(self):
        while len(self.enemies) < random.randint(3, 5): #Bis 3-5 Gegner spawnen Gegner also das hier damit 3-5 Gegner spawnen
            enemy = Enemy()
            enemy.rect.topleft = (random.randint(2, (WIDTH // TILESIZE) - 2) * TILESIZE, random.randint(2, (HEIGHT // TILESIZE) - 2) * TILESIZE) #Setzt Gegner auf Tiles
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
            self.player.handle_event(event, self.enemies) #Übergibt Ereignisse an den Spieler
    
    def update(self):
        self.player.update(self.enemies) #Aktualisiert die Position des Spielers mit Kollisionserkennung
        self.enemies.update(self.player, self.screen) #Aktualisiert alle Gegner #Übergibt screen an Gegner
        
        if not self.enemies and self.portal is None: #Wenn alle Gegner tot sind Portal erzeugen
            self.portal = pygame.Rect(random.randint(2, (WIDTH // TILESIZE) - 2) * TILESIZE, random.randint(2, (HEIGHT // TILESIZE) - 2) * TILESIZE, TILESIZE, TILESIZE) #Erstellt das Portal an zufälligem Ort in grenzen
            self.portal_image = pygame.image.load("portal.png") #Lädt das Bild für das Portal
            self.portal_image = pygame.transform.scale(self.portal_image, (TILESIZE, TILESIZE)) #Skaliert das Bild auf TILESIZE Größe

        if self.portal and self.player.rect.colliderect(self.portal): #Wenn Portal da und Spieler Rechteck berührt
            self.player.max_health += 10 #max hp wird permanentely erhöht
            self.player.health = self.player.max_health #HP reset
            self.portal = None #Entfernt das alte Portal wieder
            self.spawn_enemies() #Erstellt neue Gegner für das nächste Level
            self.player.reset_position() #Setzt den Spieler zurück zum Startpunkt
        
        if self.player.health <= 0:
            self.running = False
    
    def draw(self):
        self.screen.blit(self.background, (0, 0)) #Zeichnet den Hintergrund
        self.player.draw(self.screen) #Zeichnet den Spieler
        self.enemies.draw(self.screen) #Zeichnet alle Gegner
        if self.portal:
            self.screen.blit(self.portal_image, self.portal.topleft) #Zeichnet das Portalbild
        self.draw_health() #Zeichnet die HP-Anzeige
        for enemy in self.enemies:
            enemy.draw_health(self.screen)
            enemy.draw_damage(self.screen)
        pygame.display.flip() #Aktualisiert das Fenster
        self.clock.tick(FPS) #Setzt die Bildrate
    
    def draw_health(self):
        font = pygame.font.Font(None, 50)
        health_text = font.render("Health: " + str(self.player.health), True, (0, 255, 0)) #oder als f-string
        self.screen.blit(health_text, (30, HEIGHT - 50))  #Zeigt die Spieler-HP unten an
