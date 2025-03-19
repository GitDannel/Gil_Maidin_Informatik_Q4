#Größte Änderungen zu letzter Version:
#max health
#damage länger angezeigt
import pygame
import random
from settings import *

class Enemy(pygame.sprite.Sprite):
    #ENEMY_IMAGES = ["enemy1.png", "enemy2.png", "enemy3.png"] #Liste mit Gegnerbildern
    
    def __init__(self, game_level):
        super().__init__()
        #image_path = random.choice(self.ENEMY_IMAGES) #Zufälliges Bild aus liste auswählen
        self.image = pygame.image.load("enemy.png") #Lädt das gegnerbild #(image_path)
        self.image = pygame.transform.scale(self.image, (random.randint(40, 70), random.randint(40, 70))) #Zufällige Größe
        self.rect = self.image.get_rect(topleft=(random.randint(2, (WIDTH // TILESIZE) - 2) * TILESIZE, random.randint(2, (HEIGHT // TILESIZE) - 2) * TILESIZE)) #Macht zufällige Startposition
        #Attribute:
        self.max_health = random.randint(20, 50) + game_level * 5 #Gibt Lebenspunkte der Gegner an (skaliert mit Level)
        self.health = self.max_health
        ############################################## self.attack_range = random.randint(50, 150)
        self.attack_speed = max(random.randint(400, 600) - game_level * 20, 200) #Millisekunden zwischen Angriffen #max versichert hier dass maximal alle 200ms angreifen kann
        self.damage = random.randint(5, 15) + game_level #Schadenswert (skaliert mit Level)
        self.damage_display_time = 0 #Timer für Damage-Anzeige
        self.last_damage = 0 #Zuletzt erhaltener dmg
        self.last_attack_time = 0 #Timer (speichert wann zuletzt angegriffen wurde)


    def update(self, player, screen):
        self.attack(player) #Führt den Angriff mit Delay aus
        self.draw_health(screen)
        self.draw_damage(screen)
        #Gegnerbewegung können wir hier
    
    def attack(self, player):
        now = pygame.time.get_ticks() #Aktuelle Zeit in Millisekunden holen
        if now - self.last_attack_time > self.attack_speed: #Prüfen ob genug Zeit vergangen ist
            attack_range_x = TILESIZE * 1.5  #Größere horizontale Reichweite
            attack_range_y = TILESIZE * 1.5  #Größere vertikale Reichweite
            if abs(self.rect.centerx - player.rect.centerx) <= attack_range_x and abs(self.rect.centery - player.rect.centery) <= attack_range_y: #Hier wird die horizontale Entfernung zwischen Spieler & Gegner berechnet.
                #Falls die Entfernung kleiner als attack_range ist, kann der Angriff treffen. # abs() basically Betragsstriche
                player.health -= self.damage #Gegner verursacht Schaden am Spieler
                self.last_attack_time = now #Aktualisiert die letzte Angriffszeit
                #statt time.sleep weil ganzes Spiel irgendwie verlangsamt

    def take_damage(self, amount):
        self.health -= amount
        self.last_damage = amount
        self.damage_display_time = pygame.time.get_ticks()

    def draw_health(self, screen):
        self.font = pygame.font.Font(None, 30)
        hp_text = self.font.render(str(self.health), True, (255, 0, 0))
        screen.blit(hp_text, (self.rect.centerx - 10, self.rect.top - 20))
    
    def draw_damage(self, screen):
        self.font = pygame.font.Font(None, 30)
        if pygame.time.get_ticks() - self.damage_display_time < 150:
            dmg_text = self.font.render("-" + str(self.last_damage), True, (255, 0, 0))
            screen.blit(dmg_text, (self.rect.centerx + 20, self.rect.top - 20))

    def draw_attack_range(self, screen):
        print("Zeichne Angriff für Gegner bei " + str(self.rect.topleft)) #Debuggingzeile
        attack_range_color = (255, 0, 0, 100)
        enemy_attack_rect = pygame.Surface((TILESIZE * 3, TILESIZE * 3), pygame.SRCALPHA)
        enemy_attack_rect.fill(attack_range_color)
        screen.blit(enemy_attack_rect, (self.rect.centerx - TILESIZE * 1.5, self.rect.centery - TILESIZE * 1.5))

            

                


