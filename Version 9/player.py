#Größte Änderungen zu letzter Version:
#nur noch player collision mit blocks und nicht mehr enemies damit player nicht umzingelt und stuck ist
#if statement dass hp nicht mehr über max_hp gehen kann bei kill
#.convert_alpha und .set_colorkey damit weißer Hintergrund von Bild weg
#Auswahl aus 2 player Bildern je nachdem ob nach rechts oder links läuft
#neue player Bilder
#Tränke die man mit "2" einsetzen kann und bekommt beim enemy töten
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.character1 = pygame.image.load('character1.png').convert_alpha()
        self.character2 = pygame.image.load('character2.png').convert_alpha()
        self.character1 = pygame.transform.scale(self.character1, (TILESIZE, TILESIZE))
        self.character2 = pygame.transform.scale(self.character2, (TILESIZE, TILESIZE))
        self.character1.set_colorkey(colorkey) #Weiß transparent machen
        self.character2.set_colorkey(colorkey) #Weiß transparent machen

        # Starte mit Charakter 1
        self.current_character = self.character1
        self.image = self.current_character
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - TILESIZE))

        #Attribute:
        self.level = 1
        self.xp = 0
        self.xp_for_next_level = 100
        self.level_up_display_time = 0
        self.speed = TILESIZE // 10  #Bewegungsgeschwindigkeit ist eine Tile-Größe durch 10
        self.max_health = 500
        self.health = 500 #Lebenspunkte
        self.attack_damage = 10
        self.attack_range_x = TILESIZE * 1.5  #50% Größere horizontale Reichweite
        self.attack_range_y = TILESIZE * 1.5  #50% Größere vertikale Reichweite
        self.traenke = 0
    
    def handle_event(self, event, enemies):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: #Taste "1" für Angriff
                self.attack(enemies)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_2: #Taste "1" für Angriff
                if self.traenke >= 1:
                    self.health += 25
                    if self.health > self.max_health:
                        self.health = self.max_health
                    self.traenke -= 1
        #Hier können wir auch andere Tastatureingaben adden
    
    def attack(self, enemies):
        for enemy in enemies:
            if abs(self.rect.centerx - enemy.rect.centerx) <= self.attack_range_x and abs(self.rect.centery - enemy.rect.centery) <= self.attack_range_y: #Hier wird die horizontale Entfernung zwischen Spieler & Gegner berechnet.
                    #Falls die Entfernung kleiner als attack_range ist, kann der Angriff treffen. # abs() basically Betragsstriche
                enemy.take_damage(self.attack_damage) #Gegner verliert HP
                print("Gegner getroffen! HP: " + str(enemy.health)) #Test-Ausgabe, ob alles klappt soweit
                if enemy.health <= 0:
                    enemies.remove(enemy) #Entferne den Gegner, wenn er 0 HP hat
                    self.gain_xp(enemy.max_health)  #XP basiert auf HP des Gegners
                    self.traenke += 1
                    if self.health > self.max_health:
                        self.health = self.max_health
    
    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_for_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.xp_for_next_level *= 1.5  #XP benötigt steigt
        self.max_health += 10
        self.health = self.max_health
        self.attack_damage += 2
        self.speed += 1
        self.level_up_display_time = pygame.time.get_ticks()
        print("Level Up! Neues Level: " + str(self.level))
    
    def update(self, blocks):
        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0
        if keys[pygame.K_LEFT]:
            move_x = -self.speed #Bewegt den Spieler nach links
            self.current_character = self.character2
            self.image = self.current_character
        if keys[pygame.K_RIGHT]:
            move_x = self.speed #Bewegt den Spieler nach rechts
            self.current_character = self.character1
            self.image = self.current_character
        if keys[pygame.K_UP]:
            move_y = -self.speed #Bewegt den Spieler nach oben
        if keys[pygame.K_DOWN]:
            move_y = self.speed #Bewegt den Spieler nach unten

        #Bewegung und Kollision mit Blöcken
        #Bewegt in x-Richtung und prüft Kollisionen mit Blöcken
        self.rect.x += move_x
        for block in blocks:
            if self.rect.colliderect(block.rect):
                self.rect.x -= move_x  #Rücksetzen bei Kollision mit einem Block
                break

        #Bewegt in y-Richtung und prüft Kollisionen mit Blöcken
        self.rect.y += move_y
        for block in blocks:
            if self.rect.colliderect(block.rect):
                self.rect.y -= move_y  #Rücksetzen bei Kollision mit einem Block
                break

    def draw_level_up(self, screen):
        self.font = pygame.font.Font(None, 30)
        if pygame.time.get_ticks() - self.level_up_display_time < 250:
            level_up_text = self.font.render("LEVEL-UP", True, (255, 255, 255))
            screen.blit(level_up_text, (self.rect.centerx - 50, self.rect.top - 20))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect) #Zeichnet das Spielerbild auf den Bildschirm (Position siehe oben self.rect)
        
        
    