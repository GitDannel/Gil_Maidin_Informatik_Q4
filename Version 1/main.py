import pygame
from game import Game

def main():
    pygame.init() #Initialisiert Pygame
    game = Game() #Erstellt Instanz der Game Klasse
    game.run() #Startet das Spiel
    
if __name__ == "__main__":
    main() #Führt die main Funktion aus, wenn das Skript direkt ausgeführt wird
