class Zasoby:
    def __init__(self,drewno: int, kamien: int,zelazo: int,jedzenie: int ,jednostki: int):
        self._drewno = drewno
        self._kamien = kamien
        self._zelazo = zelazo
        self._jedzenie = jedzenie
        self._jednostki = jednostki

    def get_drewno(self): return self._drewno
    def get_kamien(self): return  self._kamien
    def get_zelazo(self): return self._zelazo
    def get_jedzenie(self): return self._jedzenie
    def get_jednostki(self): return self._jednostki

    def zmien_drewno(self, wartosc: int): self._drewno += wartosc
    def zmien_kamien(self, wartosc: int): self._kamien += wartosc
    def zmien_zelazo(self, wartosc: int): self._zelazo += wartosc
    def zmien_jedzenie(self, wartosc: int): self._jedzenie += wartosc
    def zmien_jednostki(self, wartosc: int): self._jednostki += wartosc
    def ustaw_jedzenie(self, wartosc: int): self._jednostki = wartosc