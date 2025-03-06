#Größte Änderungen zu letzter Version:
#Tilesize für Cluster für später leichter Map und Wände
import pygame
from game import Game

def main():
    pygame.init() #Initialisiert Pygame
    game = Game() #Erstellt eine Instanz der Game-Klasse
    game.run() #Startet das Spiel
    
if __name__ == "__main__":
    main() #Führt die main-Funktion aus, wenn das Skript direkt ausgeführt wird

