import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Test")

player = pygame.Rect((300, 250, 50, 50)) #xy #width height

while True:

    screen.fill((0, 0, 0)) #Hintergrund ausfüllen damit keine trail hinter sich lässt

    #Spielerfigur auf screen bringen
    pygame.draw.rect(screen, (255, 0, 0), player) #oder "Red"

    #Steuerung
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0) #move in place
    elif key[pygame.K_d] == True:
        player.move_ip(1, 0)
    if key[pygame.K_w] == True:
        player.move_ip(0, -1)
    if key[pygame.K_s] == True:
        player.move_ip(0, 1)

    # Schließen
    for event in pygame.event.get(): #durch jedes pygame event iterieren
        if event.type == pygame.QUIT:
            exit()
    
    pygame.display.update()

