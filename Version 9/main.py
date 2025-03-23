#Größte Änderungen zu letzter Version:
#startbildschirm und highscore
#Gameover hier rein
import pygame
from game import Game
from startbildschirm import Start
from gameover import Gameover
import highscore

def main():
    pygame.init() #Initialisiert Pygame
    hs = highscore.load_highscore()
    start = Start(highscore=hs)
    start.run()
    while True:
        game = Game()
        game.run()  #Spiel läuft bis der Spieler stirbt oder im Menü beendet wird
        go = Gameover(highscore=hs)
        result = go.run()  #Gameover Screen anzeigen
        
        if result == "restart":
            continue  #Neustarten
        else:
            break  #Beenden
    
    pygame.quit()
    highscore.save_highscore(game.player.level) ########################################
    
if __name__ == "__main__":
    main() #Führt die main-Funktion aus, wenn das Skript direkt ausgeführt wird
