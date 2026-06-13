class Wyposazenie:
    def __init__(self):
        self._ekwipunek ={
            "drewniana_bron":0,
            "drewniany_pancerz":0,
            "kamienna_bron":0,
            "kamienny_pancerz":0,
            "zelazna_bron":0,
            "zelazny_pancerz":0,
        }


    def get(self,nazwa:str):
        return self._ekwipunek.get(nazwa)

    def zmien(self,nazwa:str,wartosc: int):
        self._ekwipunek[nazwa]+=wartosc
