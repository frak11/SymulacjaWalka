import random

drewno_na_start:int=30
kamien_na_start:int=0
zelazo_na_start:int=0
jedzenie_na_start:int=10
jednostki_na_start: int=3
drewno_na_ture: int = 2
kamien_na_ture: int = 2
zelazo_na_ture: int = 2
jedzenie_na_ture: int = 2
koszt_ekspansji:int = 5

class Panstwo:
    def __init__(
        self, nazwa: str, stolica_x: int, stolica_y: int, agresja: float, kolor: tuple[int, int, int]
    ):
        self.nazwa = nazwa
        self.kolor = kolor
        self.agresja = agresja
        self.terytorium: set[tuple[int, int]] = {(stolica_x, stolica_y)}
        self.zasoby: dict[str, int] = {
            "drewno": drewno_na_start,
            "kamien": kamien_na_start,
            "zelazo": zelazo_na_start,
            "jedzenie": jedzenie_na_start,
            "jednostki": jednostki_na_start,
        }

    def przydziel_jednostki(self, grid_size: int, zajete_pola: set[tuple[int, int]], grid: list[list[str]]):
        pacyfizm = 1 - self.agresja
        szansa_ekspansji = self.agresja * 0.3 + pacyfizm * 0.2
        szansa_nowej_jednostki = self.agresja * 0.3 + pacyfizm * 0.1
        szansa_zelaza = self.agresja * 0.01 + pacyfizm * 0.2
        szansa_kamienia = self.agresja * 0.09 + pacyfizm * 0.2
        szansa_drewna = self.agresja * 0.2 + pacyfizm * 0.15
        szansa_jedzenia = self.agresja * 0.1 + pacyfizm * 0.15

        temp_jednostki = self.zasoby["jednostki"]
        temp_liczba_prob = 100
        while temp_jednostki > 0 and temp_liczba_prob > 0:
            chance = random.random()
            temp_liczba_prob -= 1
            if chance < szansa_ekspansji:
                if self.zasoby["drewno"] > 0:
                    self.ekspansja(grid_size, zajete_pola)
                    temp_jednostki -= 1
            elif chance < (szansa_ekspansji + szansa_nowej_jednostki):
                if self.zasoby["drewno"] > 0:
                    self.zasoby["drewno"] -= 1
                    self.zasoby["jednostki"] += 1
                    temp_jednostki -= 1
            elif chance < (szansa_ekspansji + szansa_nowej_jednostki + szansa_zelaza):
                if any(grid[y][x] == "Z" for x, y in self.terytorium):
                    if self.zasoby["kamien"] > 0:
                        self.zasoby["kamien"] -= 1
                        self.zasoby["zelazo"] += 1
                        temp_jednostki -= 1
            elif chance < (szansa_ekspansji + szansa_nowej_jednostki + szansa_zelaza + szansa_kamienia):
                if any(grid[y][x] == "K" for x, y in self.terytorium):
                    if self.zasoby["drewno"] > 0:
                        self.zasoby["drewno"] -= 1
                        self.zasoby["kamien"] += 1
                        temp_jednostki -= 1
            elif chance < (szansa_ekspansji + szansa_nowej_jednostki + szansa_zelaza + szansa_kamienia + szansa_drewna):
                if any(grid[y][x] == "D" for x, y in self.terytorium):
                    self.zasoby["drewno"] += 1
                    temp_jednostki -= 1
            elif chance < (szansa_ekspansji + szansa_nowej_jednostki + szansa_zelaza + szansa_kamienia + szansa_drewna + szansa_jedzenia):
                if any(grid[y][x] == "J" for x, y in self.terytorium):
                    self.zasoby["jedzenie"] += 5
                    temp_jednostki -= 1
        del temp_jednostki
        del temp_liczba_prob

    def utrzymanie_jednostek(self):
        if self.zasoby["jedzenie"] >= self.zasoby["jednostki"]:
            self.zasoby["jedzenie"] -= self.zasoby["jednostki"]
        else:
            self.zasoby["jednostki"] -= self.zasoby["jedzenie"]
            self.zasoby["jedzenie"] = 0

    # def zbierz_surowce(self, grid: list[list[str]]):
    #     drewno_tura = self.zasoby["drewno"]
    #     for x, y in self.terytorium:
    #         rodzaj_pola = grid[y][x]
    #         if rodzaj_pola == "D":
    #             self.zasoby["drewno"] += drewno_na_ture
    #             print(self.nazwa +"stan drewna" +str(self.zasoby["drewno"]))
    #         elif rodzaj_pola == "K":
    #             self.zasoby["kamien"] += kamien_na_ture
    #             print(self.nazwa + "stan kamienia" + str(self.zasoby["kamien"]))
    #         elif rodzaj_pola == "Z":
    #             self.zasoby["zelazo"] += zelazo_na_ture
    #             print(self.nazwa + "stan zelaza" + str(self.zasoby["zelazo"]))
    #         elif rodzaj_pola == "J":
    #             self.zasoby["jedzenie"] += jedzenie_na_ture
    #             print(self.nazwa + "stan jedzenia" + str(self.zasoby["jedzenie"]))
    #         else:
    #             pass
    #     if drewno_tura == self.zasoby["drewno"]:
    #         self.zasoby["drewno"] += 1

    def ekspansja(self, grid_size: int, zajete_pola: set[tuple[int, int]]):
        mozliwe_pola: set[tuple[int, int]] = set()
        sasiedzi=[(0,-1),(-1,0),(0,1),(1,0)]
        for x, y in self.terytorium:
            for dx, dy in sasiedzi:
                nx, ny = x+dx, y+dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    if (nx,ny) not in zajete_pola:
                        mozliwe_pola.add((nx, ny))
        if mozliwe_pola:
            losowanie_pola = random.choice(list(mozliwe_pola))
            self.terytorium.add(losowanie_pola)
            zajete_pola.add(losowanie_pola)
            self.zasoby["drewno"] -= koszt_ekspansji