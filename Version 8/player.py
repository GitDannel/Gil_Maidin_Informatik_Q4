#Größte Änderungen zu letzter Version:
#self.gain_xp(enemy.health * 2) für Lebenscaling
#draw_level_up
#Kollisionsüberprüfung jetzt auch mit Wänden bzw. blocks
import pygame
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha() #Lädt das Spielerbild
        #oder self.image.set_colorkey((255, 255, 255))  #Weiß transparent machen??
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE)) #Skaliert das Bild auf 50x50 Pixel also ein TILESIZE
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - TILESIZE)) #Macht die Startposition
        #Attribute:
        self.level = 1
        self.xp = 0
        self.xp_for_next_level = 100
        self.level_up_display_time = 0
        self.speed = TILESIZE // 10  #Bewegungsgeschwindigkeit ist eine Tile-Größe durch 10
        self.max_health = 100
        self.health = 100 #Lebenspunkte
        self.attack_damage = 10
        self.attack_range_x = TILESIZE * 1.5  #50% Größere horizontale Reichweite
        self.attack_range_y = TILESIZE * 1.5  #50% Größere vertikale Reichweite
    
    def handle_event(self, event, enemies):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: #Taste "1" für Angriff
                self.attack(enemies)
        #Hier könnten wir auch andere Tastatureingaben adden
    
    def attack(self, enemies):
        for enemy in enemies:
            if abs(self.rect.centerx - enemy.rect.centerx) <= self.attack_range_x and abs(self.rect.centery - enemy.rect.centery) <= self.attack_range_y: #Hier wird die horizontale Entfernung zwischen Spieler & Gegner berechnet.
                    #Falls die Entfernung kleiner als attack_range ist, kann der Angriff treffen. # abs() basically Betragsstriche
                enemy.take_damage(self.attack_damage) #Gegner verliert HP
                print("Gegner getroffen! HP: " + str(enemy.health)) #Test-Ausgabe, ob alles klappt soweit
                if enemy.health <= 0:
                    enemies.remove(enemy) #Entferne den Gegner, wenn er 0 HP hat
                    self.gain_xp(enemy.max_health)  #XP basiert auf HP des Gegners
                    self.health += 10 ##########################bis tränke haben
    
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
    
    def update(self, enemies, blocks):
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
        for sprite in enemies.sprites() + blocks.sprites():
            if self.rect.colliderect(sprite.rect):
                self.rect.x -= move_x
                break
        
        self.rect.y += move_y
        for sprite in enemies.sprites() + blocks.sprites():
            if self.rect.colliderect(sprite.rect):
                self.rect.y -= move_y
                break

    def draw_level_up(self, screen):
        self.font = pygame.font.Font(None, 30)
        if pygame.time.get_ticks() - self.level_up_display_time < 250:
            level_up_text = self.font.render("LEVEL-UP", True, (255, 255, 255))
            screen.blit(level_up_text, (self.rect.centerx - 50, self.rect.top - 20))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect) #Zeichnet das Spielerbild auf den Bildschirm (Position siehe oben self.rect)
        
        
    