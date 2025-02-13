#Mit Bildern

import pygame

pygame.init()

screen = pygame.display.set_mode((800, 500))

clock = pygame.time.Clock()

pygame.display.set_caption("Test")

player = pygame.image.load("Figur.jpg")
player_x = 0
player_y = 0

hintergrund = pygame.image.load("map.jpg")

text = pygame.font.Font(None, 50)
test_text = text.render("Test", True, "Red")

while True:

    screen.blit(hintergrund, (0, 0)) # screen.fill((0, 0, 0))

    
    #Spielerfigur auf screen bringen
    screen.blit(player, (player_x, player_y))
    player_x += 4
    if player_x > 800:
        player_x = -600

    screen.blit(test_text, (400, 50))

    # Schließen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    pygame.display.update()

    clock.tick(60) #max. framerate











#convert (alpha)
#warum geht auch über blit