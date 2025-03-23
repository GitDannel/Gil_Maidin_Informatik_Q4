import pygame
from settings import *

class Start:
    def __init__(self, highscore=0):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Dungeon Start")
        self.clock = pygame.time.Clock()

        #Hintergrund Bild laden
        self.background = pygame.image.load("grass.png").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))

        #Banner Bild ladem
        self.banner = pygame.image.load("banner.png").convert_alpha()
        self.banner = pygame.transform.scale(self.banner, (780, 240))
        self.banner.set_colorkey(colorkey)

        #Portal Bild laden
        self.portal = pygame.image.load("portal.png").convert_alpha()
        self.portal = pygame.transform.scale(self.portal, (150, 150))
        self.portal.set_colorkey(colorkey)

        self.highscore = highscore  #wird bei Init Klammer übergeben

    def run(self):
        while True:
            self.screen.fill((0, 120, 0))

            #Hintergrund anzeigen
            self.screen.blit(self.background, (0, 0))

            #Banner anzeigem
            self.screen.blit(self.banner, (20, 0))

            #Überschrift auf Banner zeichnen
            self.title_font = pygame.font.Font(None, 90) #große Überschrift
            title = self.title_font.render("Dungeons & Dungeons", True, (0, 0, 0))
            self.screen.blit(title, (20 + self.banner.get_width() // 2 - title.get_width() // 2, 0 + self.banner.get_height() // 2 - title.get_height() // 2)) #x y #diese 20 und 0 kommen von da oben wo der banner platziert wird
            
            #Portal Bild anzeigen
            self.screen.blit(self.portal, (325, 210))  #zentriert unter  Titel

            #Highscore anzeigen
            self.highscore_font = pygame.font.Font(None, 36)
            score_text = self.highscore_font.render("Highscore: Level " + str(self.highscore), True, (255, 255, 255))
            self.screen.blit(score_text, (400 - score_text.get_width() // 2, 420))

            #für buttons
            mouse_pos = pygame.mouse.get_pos()

            #Start Button mit Hover Effekt
            self.button_rect = pygame.Rect(300, 450, 200, 80)

            if self.button_rect.collidepoint(mouse_pos):
                color = (50, 50, 50)
            else:
                color = (0, 0, 0)
            pygame.draw.rect(self.screen, color, self.button_rect)
            #
            self.button_font = pygame.font.Font(None, 60)
            text = self.button_font.render("Start", True, (255, 255, 255))
            self.screen.blit(text, (self.button_rect.x + 40, self.button_rect.y + 20))

            #Quit Button mit Hover Effekt
            self.quit_button_rect = pygame.Rect(575, 450, 200, 80) #Quit-Button bisschen unter dem Start-Button

            if self.quit_button_rect.collidepoint(mouse_pos):
                quit_color = (50, 50, 50)
            else:
                quit_color = (0, 0, 0)
            pygame.draw.rect(self.screen, quit_color, self.quit_button_rect)
            #
            self.button_font = pygame.font.Font(None, 60)
            quit_text = self.button_font.render("Quit", True, (255, 255, 255))
            self.screen.blit(quit_text, (self.quit_button_rect.x + (self.quit_button_rect.width - quit_text.get_width()) // 2, self.quit_button_rect.y + (self.quit_button_rect.height - quit_text.get_height()) // 2))

            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        return  #Spiel starten
                    elif self.quit_button_rect.collidepoint(event.pos):
                        pygame.quit()

            pygame.display.flip()
            self.clock.tick(FPS)