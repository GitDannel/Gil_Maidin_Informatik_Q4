import pygame
import random
import math
from settings import *

class Enemy(pygame.sprite.Sprite):
    ENEMY_IMAGES = ["enemy1.png", "enemy2.png"] #Liste mit Gegnerbildern
    
    def __init__(self, game_level):
        super().__init__()
        self.image = pygame.image.load(random.choice(self.ENEMY_IMAGES)).convert() #Lädt gegnerbild durch zufälliges Bild aus liste auswählen #(image_path)
        self.image.set_colorkey(colorkey)
        self.image = pygame.transform.scale(self.image, (random.randint(40, 70), random.randint(40, 70))) #Zufällige Größe
        self.rect = self.image.get_rect(topleft=(random.randint(2, (WIDTH // TILESIZE) - 2) * TILESIZE, random.randint(2, (HEIGHT // TILESIZE) - 2) * TILESIZE)) #Macht zufällige Startposition

        #Attribute:
        self.max_health = random.randint(20, 50) + game_level * 5 #Gibt Lebenspunkte der Gegner an (skaliert mit Level)
        self.health = self.max_health
        # self.attack_range = random.randint(50, 150)
        self.attack_speed = max(random.randint(400, 600) - game_level * 20, 200) #Millisekunden zwischen Angriffen #max versichert hier dass maximal alle 200ms angreifen kann
        self.damage = random.randint(5, 15) + game_level #Schadenswert (skaliert mit Level)
        self.damage_display_time = 0 #Timer für Damage-Anzeige
        self.last_damage = 0 #Zuletzt erhaltener dmg
        self.last_attack_time = 0 #Timer (speichert wann zuletzt angegriffen wurde)

        #Bewegung
        self.speed = 2  #Geschwindigkeit Gegner
        #zufällige Richtung: -1 (links/hoch), 0 (keine Bewegung) oder 1 (rechts/runter)
        self.direction_x = random.choice([-1, 0, 1])  # Bewegungsrichtung in x-Richtung
        self.direction_y = random.choice([-1, 0, 1])  # Bewegungsrichtung in y-Richtung
        if self.direction_x == 0 and self.direction_y == 0:
            self.direction_x = 1  #Falls beide 0 sind, wird dx auf 1 gesetzt um Bewegung zu erzwingen
        self.last_direction_change = pygame.time.get_ticks()  #Merkt sich wann die Richtung zuletzt geändert wurde
        self.chase_distance = 200  #Wenn der Spieler näher als 200 Pixel ist wird er verfolgt

        self.distance = 0  #Standardwert falls noch kein Abstand berechnet wurde

    def update(self, player, screen, blocks, enemies):
        self.move(player, blocks, enemies)  #Bewegung ausführen
        self.attack(player) #Führt den Angriff mit Delay aus
        self.draw_health(screen) #Zeigt Gesundheit an
        self.draw_damage(screen) #Zeigt bekommenen damage kurz an
        self.draw_aggro(screen)

    def move(self, player, blocks, enemies):
        #Berechne den Abstand zum Spieler mit math.hypot (Pythagoras)
        self.distance = math.hypot(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        
        if self.distance < self.chase_distance:
            #Spieler verfolgen
            #Berechnet Unterschied in x und y
            diff_x = player.rect.centerx - self.rect.centerx
            diff_y = player.rect.centery - self.rect.centery
            #Setzt dx und dy so, dass der Gegner in Richtung des Spielers geht
            if diff_x != 0:
                self.direction_x = diff_x / abs(diff_x)  #Ergibt -1 oder 1
            if diff_y != 0:
                self.direction_y = diff_y / abs(diff_y)  #Ergibt -1 oder 1
        else:
            #Zufällige Bewegung
            now = pygame.time.get_ticks()  #Aktuelle Zeit in Millisekunden
            #Wenn mehr als 1000ms um sind, ändere die Richtung zufällig
            if now - self.last_direction_change > 1000:
                self.direction_x = random.choice([-1, 0, 1])
                self.direction_y = random.choice([-1, 0, 1])
                if self.direction_x == 0 and self.direction_y == 0:
                    self.direction_x = 1  #Erzwingt Bewegung wenn beide 0 sind
                self.last_direction_change = now  #Aktualisiert Zeitding

            #Kollision mit Gegnern (Stehenbleiben)
        for enemy in enemies:
            if self.rect.colliderect(player.rect):
                return

        #Speichere aktuelle Position damit wir sie bei einer Kollision zurücksetzen können
        old_x = self.rect.x
        old_y = self.rect.y

        #Bewegung in x-Richtung
        self.rect.x += self.direction_x * self.speed  #Gegner in x-Richtung
        #Prüft für jeden Block ob eine Kollision stattfindet
        for block in blocks:
            if self.rect.colliderect(block.rect):
                self.rect.x = old_x  #Setze die x-Position zurück, wenn Kollision
                self.direction_x = -self.direction_x  #Kehre x-Richtung um (einfach Vorzeichenwechsel)
                break  #Beende die Schleife weil Kollision gefunden wurde

        #Bewegung in y-Richtung
        self.rect.y += self.direction_y * self.speed  #Gegner in y-Richtung
        #Prüft für jeden Block ob eine Kollision stattfindet
        for block in blocks:
            if self.rect.colliderect(block.rect):
                self.rect.y = old_y  #Setzt die y-Position zurück, wenn Kollision
                self.dircetion_y = -self.direction_y  #Kehre die y-Richtung um
                break  #Beende Schleife weil Kollision gefunden wurde
    
    def attack(self, player):
        now = pygame.time.get_ticks() #Aktuelle Zeit in Millisekunden holen
        # Standardmäßig wird angenommen, dass kein Angriff stattgefunden hat
        # self.just_attacked = False  
        if now - self.last_attack_time > self.attack_speed: #Prüfen ob genug Zeit vergangen ist
            self.attack_range_x = TILESIZE * 1.5 #Größere horizontale Reichweite
            self.attack_range_y = TILESIZE * 1.5 #Größere vertikale Reichweite
            #greift an sobald Gegner in Reichweite ist (also macht constant damage einfach):
            if abs(self.rect.centerx - player.rect.centerx) <= self.attack_range_x and abs(self.rect.centery - player.rect.centery) <= self.attack_range_y: #Hier wird die horizontale Entfernung zwischen Spieler & Gegner berechnet.
                #Falls die Entfernung kleiner als attack_range ist, kann der Angriff treffen. # abs() basically Betragsstriche
                player.health -= self.damage #Gegner verursacht Schaden am Spieler
                self.last_attack_time = now #Aktualisiert die letzte Angriffszeit
                #statt time.sleep weil ganzes Spiel irgendwie verlangsamt
                # self.just_attacked = True # Sagt jetzt, dass ein Angriff stattgefunden hat

    def take_damage(self, amount):
        self.health -= amount
        self.last_damage = amount
        self.damage_display_time = pygame.time.get_ticks()

        

    ####################################
    #drawen

    def draw_health(self, screen):
        self.font = pygame.font.Font(None, 30)
        hp_text = self.font.render(str(self.health), True, (255, 0, 0))
        screen.blit(hp_text, (self.rect.centerx - 10, self.rect.top - 20))
    
    def draw_damage(self, screen):
        self.font = pygame.font.Font(None, 30)
        if pygame.time.get_ticks() - self.damage_display_time < 150:
            dmg_text = self.font.render("-" + str(self.last_damage), True, (255, 0, 0))
            screen.blit(dmg_text, (self.rect.centerx + 20, self.rect.top - 20))

    def draw_aggro(self, screen):
        self.font = pygame.font.Font(None, 50)
        aggro_text = self.font.render("!", True, (255, 0, 0))
        screen.blit(aggro_text, (self.rect.left - 15, self.rect.centery - 15))

    def draw_attack_range(self, screen):
        print("Zeichne Angriff für Gegner bei " + str(self.rect.topleft)) #Debuggingzeile
        attack_range_color = (255, 0, 0, 100)
        enemy_attack_rect = pygame.Surface((TILESIZE * 3, TILESIZE * 3), pygame.SRCALPHA)
        enemy_attack_rect.fill(attack_range_color)
        screen.blit(enemy_attack_rect, (self.rect.centerx - TILESIZE * 1.5, self.rect.centery - TILESIZE * 1.5))

            

                


