#Größte Änderungen zu letzter Version:
#Variable self.show_attack_ranges und Methode self.draw_attack_ranges damit man Tab drücken kann für attack ranges sehen - man sieht wird nur in Mitte gehittet
#draw_level, draw_xp um unten hinzuschreiben
#############
#Variable game_level für game Levels
#next_level und spawn_portal für Simplifizierung
#spawn_enemies umgeschrieben sodass da die Anzahl jetzt auch scalen kann
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
        self.show_attack_range = False  # Anzeige der Angriffsreichweite
        self.game_level = 1
        self.spawn_enemies() #Erstellt die Gegner beim Spielstart
    
    def spawn_enemies(self):
        num_enemies = random.randint(3 + self.game_level, 5 + self.game_level)  #Mehr Gegner je Level
        for i in range(num_enemies):
            enemy = Enemy(self.game_level)
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    print("TAB gedrückt") #Debuggingzeile
                    self.show_attack_range = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    print("TAB losgelassen") #Debuggingzeile
                    self.show_attack_range = False
            self.player.handle_event(event, self.enemies) #Übergibt Ereignisse an den Spieler
    
    def update(self):
        self.player.update(self.enemies) #Aktualisiert die Position des Spielers mit Kollisionserkennung
        self.enemies.update(self.player, self.screen) #Aktualisiert alle Gegner #Übergibt screen an Gegner
        
        if not self.enemies and self.portal is None: #Wenn alle Gegner tot sind Portal erzeugen
            self.spawn_portal()

        if self.portal and self.player.rect.colliderect(self.portal): #Wenn Portal da und Spieler Rechteck berührt
            self.next_level()
        
        if self.player.health <= 0:
            self.running = False
    
    def spawn_portal(self):
        self.portal = pygame.Rect(random.randint(2, (WIDTH // TILESIZE) - 2) * TILESIZE, random.randint(2, (HEIGHT // TILESIZE) - 2) * TILESIZE, TILESIZE, TILESIZE) #Erstellt das Portal an zufälligem Ort in grenzen
        self.portal_image = pygame.image.load("portal.png") #Lädt das Bild für das Portal
        self.portal_image = pygame.transform.scale(self.portal_image, (TILESIZE, TILESIZE)) #Skaliert das Bild auf TILESIZE Größe

    def next_level(self):
        #self.player.max_health += 10 #max hp wird permanentely erhöht
        self.player.health = self.player.max_health #HP reset
        self.portal = None #Entfernt das alte Portal wieder
        self.game_level += 1
        self.spawn_enemies() #Erstellt neue Gegner für das nächste Level
        self.player.reset_position() #Setzt den Spieler zurück zum Startpunkt



    #######################################
    #drawen:

    def draw(self):
        self.screen.blit(self.background, (0, 0)) #Zeichnet den Hintergrund
        self.player.draw(self.screen) #Zeichnet den Spieler
        self.enemies.draw(self.screen) #Zeichnet alle Gegner
        if self.portal:
            self.screen.blit(self.portal_image, self.portal.topleft) #Zeichnet das Portalbild
        self.draw_health() #Zeichnet die HP-Anzeige
        self.draw_level()
        self.draw_xp()
        for enemy in self.enemies:
            enemy.draw_health(self.screen)
            enemy.draw_damage(self.screen)
        if self.show_attack_range:
            self.draw_attack_ranges()
        pygame.display.flip() #Aktualisiert das Fenster
        self.clock.tick(FPS) #Setzt die Bildrate
    
    def draw_health(self):
        font = pygame.font.Font(None, 50)
        health_text = font.render("Health: " + str(self.player.health), True, (0, 255, 0)) #oder als f-string
        self.screen.blit(health_text, (500, HEIGHT - 35))  #Zeigt die Spieler-HP unten an

    def draw_level(self):
        font = pygame.font.Font(None, 50)
        level_text = font.render("Level: " + str(self.player.level), True, (0, 255, 0)) #oder als f-string
        self.screen.blit(level_text, (15, HEIGHT - 40))  #Zeigt Spielerlevel unten an

    def draw_xp(self):
        font = pygame.font.Font(None, 50)
        xp_text = font.render("XP: " + str(self.player.xp), True, (0, 255, 0)) #oder als f-string
        self.screen.blit(xp_text, (15, HEIGHT - 75))  #Zeigt die Spieler-XP unten an
    
    def draw_attack_ranges(self):
        print("Zeichne Angriffsreichweiten") #Test ob die Funktion übrhaupt läuft
        attack_range_color = (0, 255, 0, 100)
        player_attack_rect = pygame.Surface((TILESIZE * 3, TILESIZE * 3), pygame.SRCALPHA)
        player_attack_rect.fill(attack_range_color)
        self.screen.blit(player_attack_rect, (self.player.rect.centerx - TILESIZE * 1.5, self.player.rect.centery - TILESIZE * 1.5))
        
        for enemy in self.enemies:
            enemy.draw_attack_range(self.screen)
    


