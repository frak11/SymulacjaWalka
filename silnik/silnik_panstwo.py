import random

from pygame.examples import grid

drewno_na_start:int=30
kamien_na_start:int=0
zelazo_na_start:int=0
jedzenie_na_start:int=10
drewno_na_ture: int = 2
kamien_na_ture: int = 2
zelazo_na_ture: int = 2
jedzenie_na_ture: int = 2
koszt_ekspansji:int =10

class Panstwo:
    def __init__(
        self, nazwa: str, stolica_x: int, stolica_y: int, kolor: tuple[int, int, int]
    ):
        self.nazwa = nazwa
        self.kolor = kolor
        self.terytorium: set[tuple[int, int]] = {(stolica_x, stolica_y)}
        self.zasoby: dict[str, int] = {
            "drewno": drewno_na_start,
            "kamien": kamien_na_start,
            "zelazo": zelazo_na_start,
            "jedzenie": jedzenie_na_start,
        }

    def zbierz_surowce(self, grid: list[list[str]]):
        drewno_tura = self.zasoby["drewno"]
        for x, y in self.terytorium:
            rodzaj_pola = grid[y][x]
            if rodzaj_pola == "D":
                self.zasoby["drewno"] += drewno_na_ture
                print(self.nazwa +"stan drewna" +str(self.zasoby["drewno"]))
            elif rodzaj_pola == "K":
                self.zasoby["kamien"] += kamien_na_ture
                print(self.nazwa + "stan kamienia" + str(self.zasoby["kamien"]))
            elif rodzaj_pola == "Z":
                self.zasoby["zelazo"] += zelazo_na_ture
                print(self.nazwa + "stan zelaza" + str(self.zasoby["zelazo"]))
            elif rodzaj_pola == "J":
                self.zasoby["jedzenie"] += jedzenie_na_ture
                print(self.nazwa + "stan jedzenia" + str(self.zasoby["jedzenie"]))
            else:
                pass
        if drewno_tura == self.zasoby["drewno"]:
            self.zasoby["drewno"] += 1
    def ekspansja(self,grid_size: int,zajete_pola: set[tuple[int, int]]):
        if self.zasoby["drewno"] <koszt_ekspansji:
            return
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
            print(self.nazwa +" zajelo nowe pole " +   "pozostałe drewno:" + str(self.zasoby["drewno"]))



        
