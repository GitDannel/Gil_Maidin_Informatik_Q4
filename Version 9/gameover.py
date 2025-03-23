import pygame
from settings import *

class Gameover:
    def __init__(self, highscore=0):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Game Over")
        self.clock = pygame.time.Clock()

        #Hintergrundbild
        self.background = pygame.image.load("grass.png").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))

        self.highscore = highscore  #wird bei Init Klammer übergeben

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))
            
            #"GAME OVER" Text in Rot ganz gro´ß zentral
            self.title_font = pygame.font.Font(None, 100) #Große Schrift für "GAME OVER"
            game_over_text = self.title_font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(game_over_text, ((800 - game_over_text.get_width()) // 2, 100))

            #Highscore anzeigen
            self.highscore_font = pygame.font.Font(None, 36)
            score_text = self.highscore_font.render("Dein aktueller Highscore: Level " + str(self.highscore), True, (255, 255, 255))
            self.screen.blit(score_text, (200, 275))
            
            #Buttons zeichnen (mit coolem Farben ändern Hover-Effekt)
            mouse_pos = pygame.mouse.get_pos()

            self.restart_button = pygame.Rect(150, 450, 200, 80)
            if self.restart_button.collidepoint(mouse_pos):
                restart_color = (50, 50, 50)
            else:
                restart_color = (0, 0, 0)
            pygame.draw.rect(self.screen, restart_color, self.restart_button)

            self.quit_button = pygame.Rect(450, 450, 200, 80)
            if self.quit_button.collidepoint(mouse_pos):
                quit_color = (50, 50, 50)
            else:
                quit_color = (0, 0, 0)
            if self.quit_button.collidepoint(mouse_pos):
                quit_color = (50, 50, 50)
            else:
                quit_color = (0, 0, 0)
            quit_color = (50, 50, 50) if self.quit_button.collidepoint(mouse_pos) else (0, 0, 0)
            pygame.draw.rect(self.screen, quit_color, self.quit_button)
            
            #Buttontexte in buttons mittig
            self.button_font = pygame.font.Font(None, 60) #Schrift für Buttons
            restart_text = self.button_font.render("Restart", True, (255, 255, 255))
            quit_text = self.button_font.render("Quit", True, (255, 255, 255))
            self.screen.blit(restart_text, (self.restart_button.x + (self.restart_button.width - restart_text.get_width()) // 2, self.restart_button.y + (self.restart_button.height - restart_text.get_height()) // 2))
            self.screen.blit(quit_text, (self.quit_button.x + (self.quit_button.width - quit_text.get_width()) // 2, self.quit_button.y + (self.quit_button.height - quit_text.get_height()) // 2))
            
            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_button.collidepoint(event.pos):
                        return "restart"
                    elif self.quit_button.collidepoint(event.pos):
                        return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "restart"
                    elif event.key == pygame.K_q:
                        return "quit"
                        
            pygame.display.flip()
            self.clock.tick(FPS)