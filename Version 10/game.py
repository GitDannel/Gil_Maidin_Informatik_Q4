import pygame
from player import Player
from enemy import Enemy
from settings import *
from tilemap import *
from block import Block
import random

class Game:
    def __init__(self):
        # info = pygame.display.Info()
        # self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN) #Erstellt das Spielfenster
        # print("Bildschirmauflösung:", info.current_w, "x", info.current_h)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN) #Erstellt das Spielfenster

        # # Aktuelle Bildschirmauflösung abrufen:
        # info = pygame.display.Info()
        # width, height = info.current_w, info.current_h

        # # Fenster im "fullscreen windowed"-Modus erstellen:
        # self.screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption("Dungeon Game") #Gibt den Fenstertitel an

        self.clock = pygame.time.Clock() #Erstellt eine clock für die Framerate
        self.running = True #Variable für die Spielschleife

        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, (TILESIZE * (WIDTH // TILESIZE), TILESIZE * (HEIGHT // TILESIZE))) #Passt den Hintergrund an die Tile Größe an

        self.banner = pygame.image.load("banner.png").convert_alpha()
        self.banner = pygame.transform.scale(self.banner, (300, 100))
        self.banner.set_colorkey(colorkey)

        #für unten draw_attack:
        self.player_schlag = pygame.image.load("explosion.png").convert_alpha() #Bild laden
        self.player_schlag.set_colorkey(colorkey)
        self.player_schlag = pygame.transform.scale(self.player_schlag, (TILESIZE * 3, TILESIZE * 3))

        self.player = Player() #Erstellt den Spieler
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group() #Erstellt eine leere Gegner Gruppe
        self.blocks = pygame.sprite.Group()
        self.portal = None  #Portal wird erst erstellt wenn alle Gegner besiegt sind
        self.show_attack_range = False  #Anzeige Angriffsreichweite
        self.game_level = 1

    def create_tilemap(self): #i ist die position, row ist der value
        chosen_tilemap = random.choice(tilemaps)  # Wählt zufällig eine Tilemap aus
        for i, row in enumerate(chosen_tilemap):
            #print(i, row)
            for j, column in enumerate(row):
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    self.player.rect.topleft = (j * TILESIZE, i * TILESIZE)
    
    def spawn_enemies(self):
        num_enemies = random.randint(1 + self.game_level, 3 + self.game_level) #Mehr Gegner je Level
        for i in range(num_enemies):
            valid_position = False
            while not valid_position:
                enemy = Enemy(self.game_level)
                enemy.rect.topleft = (random.randint(2, (WIDTH // TILESIZE) - 2) * TILESIZE, random.randint(2, (HEIGHT // TILESIZE) - 2) * TILESIZE) #Setzt Gegner auf Tiles
                #dass Gegner nicht mehr in Wand/block oder direkt beim Spieler spawnen
                if enemy.rect.colliderect(self.player.rect): #Wenn erzeugter Gegner nicht kollidiert mit Spieler Rechteck
                    print("1")
                    continue  #Ungültig, nächste Position
                #Erzeugt range um den Spieler
                no_spawn_zone = self.player.rect.inflate(TILESIZE * 2, TILESIZE * 2)
                if enemy.rect.colliderect(no_spawn_zone):
                    print("2")
                    continue  #Zu nah am Spieler, neue Position wählen

                #Prüft ob der Gegner in einem Block spawnt
                collision_with_block = False
                for block in self.blocks:
                    if enemy.rect.colliderect(block.rect):
                        collision_with_block = True
                        break
                if collision_with_block:
                    print("3")
                    continue  #Position darf nicht weil in einem Block

                valid_position = True  #Alle Prüfungen bestanden

            self.enemies.add(enemy) #dann wird Gruppe hinzugefügt
    
    def run(self):
        self.create_tilemap()
        self.spawn_enemies() #Erstellt die Gegner beim Spielstart
        while self.running:
            self.handle_events() #Verarbeitet Benutzer-Eingaben
            self.update() #Aktualisiert das Spielgeschehen
            self.draw() #Zeichnet also quasi setzt die Elemente auf den Bildschirm
        # pygame.quit() #Beendet Pygame wenn die Schleife stoppt #rausgenommen weil sonst mit gameover nicht mehr klappt

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False #Schließt das Spiel wenn das Fenster geschlossen wird
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_menu()  #Pause-Menü aufrufen
                if event.key == pygame.K_TAB:
                    print("TAB gedrückt") #Debuggingzeile
                    self.show_attack_range = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    print("TAB losgelassen") #Debuggingzeile
                    self.show_attack_range = False
            self.player.handle_event(event, self.enemies) #Übergibt Ereignisse an den Spieler
        
    def pause_menu(self):
        paused = True
        #Definiere die Button-Rechtecke
        resume_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50)
        quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50)
        
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    paused = False
                elif event.type == pygame.KEYDOWN:
                    #Mit ESC lässt sich auch wieder fortsetzen
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.collidepoint(event.pos):
                        paused = False  #Spiel fortsetzen
                    elif quit_button.collidepoint(event.pos):
                        self.running = False  #Spiel beenden
                        paused = False
            
            # # Zeichne den Pause-Overlay
            # overlay = pygame.Surface((WIDTH, HEIGHT))
            # overlay.set_alpha(128)  #legt alphawert vom Pause overlay fest also oberfläche transparenz geht von 0 also voll durchsichtig bis 255
            # overlay.fill((0, 0, 0)) #bräuchten wir wenn wir nicht komplett durchsichtig machen also Farbe vom Hintergrund overlay hinter Knöpfen
            # self.screen.blit(overlay, (0, 0))
            
            #Buttons zeichnen
            pygame.draw.rect(self.screen, (100, 100, 100), resume_button)
            pygame.draw.rect(self.screen, (100, 100, 100), quit_button)
            font = pygame.font.Font(None, 50)
            resume_text = font.render("Fortsetzen", True, (255, 255, 255))
            quit_text = font.render("Beenden", True, (255, 255, 255))
            self.screen.blit(resume_text, (resume_button.x + 10, resume_button.y + 10))
            self.screen.blit(quit_text, (quit_button.x + 10, quit_button.y + 10))
            
            pygame.display.flip()
            self.clock.tick(15)
    
    def update(self):
        self.player.update(self.blocks) #Aktualisiert Position des Spielers mit Kollisionserkennung
        self.enemies.update(self.player, self.screen, self.blocks, self.enemies) #Aktualisiert alle Gegner #Übergibt screen an Gegner
        
        if not self.enemies and self.portal is None: #Wenn alle Gegner tot sind Portal erzeugen
            self.spawn_portal()

        if self.portal and self.player.rect.colliderect(self.portal): #Wenn Portal da und Spieler Rechteck berührt
            self.next_level()
        
        if self.player.health <= 0:
            self.player.health = 0 #damit da keine negative Zahl steht
            print("gestorben") #Zur Überprüfung ob gestorben
            self.running = False
    
    def spawn_portal(self):
        valid_position = False
        while not valid_position:
            self.portal = pygame.Rect(random.randint(2, (WIDTH // TILESIZE) - 2) * TILESIZE, random.randint(2, (HEIGHT // TILESIZE) - 2) * TILESIZE, 3*TILESIZE, 3*TILESIZE) #Erstellt das Portal an zufälligem Ort in grenzen
            #Prüft ob das Portal den Spieler berührt oder in No-Spawn-Zone liegt:
            if self.portal.colliderect(self.player.rect):
                continue
            no_spawn_zone = self.player.rect.inflate(TILESIZE * 2, TILESIZE * 2)
            if self.portal.colliderect(no_spawn_zone):
                continue
            #Prüft ob das Portal in einem Block spawnt:
            collision_with_block = False
            for block in self.blocks:
                if self.portal.colliderect(block.rect):
                    collision_with_block = True
                    break
            if collision_with_block:
                continue
            valid_position = True
        self.portal_image = pygame.image.load("portal.png") #Lädt das Bild für das Portal
        self.portal_image.set_colorkey(colorkey)
        self.portal_image = pygame.transform.scale(self.portal_image, (3*TILESIZE, 3*TILESIZE)) #Skaliert das Bild auf TILESIZE Größe bzw. halt auf Größe vom rectangle
        

    def next_level(self):
        # self.player.max_health += 10 #max hp wird permanentely erhöht
        self.player.health = self.player.max_health #HP reset
        self.portal = None #Entfernt das alte Portal wieder
        self.game_level += 1
        self.blocks.empty() #damit sich maps nicht "adden" und ab ca. 3.Level nur noch eine kommt immer
        self.all_sprites.empty()
        self.create_tilemap() #Erstellt neue map für das nächste Level
        self.spawn_enemies() #Erstellt neue Gegner für das nächste Level



    #######################################
    #drawen:

    def draw(self):
        self.screen.blit(self.background, (0, 0)) #Zeichnet den Hintergrund
        self.player.draw(self.screen) #Zeichnet den Spieler
        self.enemies.draw(self.screen) #Zeichnet alle Gegner
        self.blocks.draw(self.screen)
        #
        if self.portal:
            self.screen.blit(self.portal_image, self.portal.topleft) #Zeichnet das Portalbild
        #
        self.draw_game_level()
        
        self.draw_health() #Zeichnet die HP-Anzeige
        self.draw_level()
        self.draw_xp()
        self.draw_traenke()
        self.player.draw_level_up(self.screen)
        #
        for enemy in self.enemies:
            enemy.draw_health(self.screen)
            enemy.draw_damage(self.screen)
            #
            if enemy.distance < enemy.chase_distance:
                enemy.draw_aggro(self.screen)
            # if enemy.just_attacked:
            #     enemy.draw_attack_range(self.screen)
        #
        if self.show_attack_range:
            self.draw_attack_ranges()
        #
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.draw_attack()
        #
        pygame.display.flip() #Aktualisiert das Fenster
        self.clock.tick(FPS) #Setzt die Bildrate

    ######################

    #game level auf Banner zeichnen
    def draw_game_level(self):
        #Banner anzeigen
        self.screen.blit(self.banner, (20, 0))

        font = pygame.font.Font(None, 50)
        game_level_text = font.render("Game-Level " + str(self.game_level), True, (0, 0, 0))
        self.screen.blit(game_level_text, (20 + self.banner.get_width() // 2 - game_level_text.get_width() // 2, 0 + self.banner.get_height() // 2 - game_level_text.get_height() // 2)) #x y

    ######################
    #player
    def draw_health(self):
        font = pygame.font.Font(None, 50)
        health_text = font.render("Health: " + str(self.player.health) + "/" + str(self.player.max_health), True, (0, 255, 0))
        self.screen.blit(health_text, (500, HEIGHT - 35))  #Zeigt die Spieler-HP unten an

    def draw_level(self):
        font = pygame.font.Font(None, 50)
        level_text = font.render("Level: " + str(self.player.level), True, (0, 255, 0))
        self.screen.blit(level_text, (15, HEIGHT - 40))  #Zeigt Spielerlevel unten an

    def draw_xp(self):
        font = pygame.font.Font(None, 50)
        xp_text = font.render("XP: " + str(round(self.player.xp)) + "/" + str(round(self.player.xp_for_next_level)), True, (0, 255, 0))
        self.screen.blit(xp_text, (15, HEIGHT - 75))  #Zeigt die Spieler-XP unten an
    
    def draw_traenke(self):
        font = pygame.font.Font(None, 50)
        traenke_text = font.render("Tränke: " + str(self.player.traenke), True, (0, 255, 0))
        self.screen.blit(traenke_text, (15, HEIGHT - 110))  #Zeigt die Spieler-XP unten an

    def draw_attack(self):
        #Kopie erstellen, auf der wir die Transparenz setzen
        player_schlag_alpha = self.player_schlag.copy()
        player_schlag_alpha.set_alpha(200)  # 0 = komplett transparent, 255 = voll sichtbar
        self.screen.blit(player_schlag_alpha, (self.player.rect.centerx - TILESIZE * 1.5, self.player.rect.centery - TILESIZE * 1.5))
        
    def draw_attack_range(self):
        attack_range_color = (0, 255, 0, 100)
        player_attack_rect = pygame.Surface((TILESIZE * 3, TILESIZE * 3), pygame.SRCALPHA)
        player_attack_rect.fill(attack_range_color)
        self.screen.blit(player_attack_rect, (self.player.rect.centerx - TILESIZE * 1.5, self.player.rect.centery - TILESIZE * 1.5))



    #
    def draw_attack_ranges(self):
        print("Zeichne Angriffsreichweiten") #Test ob die Funktion übrhaupt läuft

        self.draw_attack_range()
        
        for enemy in self.enemies:
            enemy.draw_attack_range(self.screen)



    