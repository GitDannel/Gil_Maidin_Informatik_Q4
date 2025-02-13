#movement

import pygame

pygame.init()

screen = pygame.display.set_mode((800, 500))

clock = pygame.time.Clock()

pygame.display.set_caption("Test")

hintergrund = pygame.image.load("map.jpg")

player_surface = pygame.image.load("Figur.jpg")
player_surface = pygame.transform.scale(player_surface, (50, 50))
player_rectangle = player_surface.get_rect(bottomleft = (0, 410)) ###statt midbottom

gegner_surface = pygame.image.load("Figur.jpg")
gegner_surface = pygame.transform.scale(gegner_surface, (50, 50))
gegner_rectangle = gegner_surface.get_rect(midbottom = (500, 410))

text = pygame.font.Font(None, 50)
test_text = text.render("Test", True, "Red")

running = True

while running:

    screen.blit(hintergrund, (0, 0))

    #Figuren auf screen bringen
    screen.blit(player_surface, player_rectangle)
    screen.blit(gegner_surface, gegner_rectangle)

    # print(player_rectangle.colliderect(gegner_rectangle))

    #Steuerung
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player_rectangle.move_ip(-4, 0)
    elif key[pygame.K_d] == True:
        player_rectangle.move_ip(4, 0)
    if key[pygame.K_w] == True:
        player_rectangle.move_ip(0, -4)
    if key[pygame.K_s] == True:
        player_rectangle.move_ip(0, 4)

    #Auf anderer Seite wieder raus
    if player_rectangle.left >= 800:
        player_rectangle.right = 0
    
    if player_rectangle.colliderect(gegner_rectangle):
        running = False

    screen.blit(test_text, (400, 50))

    # Schließen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()

    clock.tick(60)


    