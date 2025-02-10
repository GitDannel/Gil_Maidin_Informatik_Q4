class Spielfeld:
    def __init__(self, breite:int="0", höhe:int"0"):
        self.__breite = breite
        self.__höhe = höhe
        self.felder = [[None for _ in range(breite)] for _ in range(höhe)]
        
    def ist:gueltige_position(self, breite, höhe):
        return 0<=breite< self.__breite and 0< höhe < self.__höhe
        
    def setze_objekt(self, breite, höhe, objekt):
        if self.ist_gueltig_position(breite, höhe): #kein check ob besetzt
            self.felder[höhe][breite]
            
    def entferne_objekt(self, breite, höhe):
        if self.ist_gueltig_position(breite, höhe):
            self._felder[höhe][breite] = None
            asdasdadsadsadsads
    def __str__
            
        
ssssssssssssssssssssssssssssssssssssssssssssss
