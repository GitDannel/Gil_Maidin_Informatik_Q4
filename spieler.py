from Spielfel import Spielfeld

class Spieler:
    def __init__(self, richtung:str="^", breite:int="0", höhe:int="0"):
        self.__spielfeld = spielfeld
        self.__breite = 0
        self.__höhe = 0
        
        
    def rechts(self, entfrenung):
        breite += entfernung
        self.richtung = ">"
        
    def links(self, entfrenung):
        breite -= entfernung
        self.richtung = "<"
        
    def oben(self, entfrenung):
        höhe += entfernung
        self.richtung = "^"
        
     def unten(self, entfernung):
         höhe -= entfernung
         self.richtung = "v"