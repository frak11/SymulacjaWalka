import math
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

ilosc_jedzenia_z_pola: int = 3
ilosc_drewna_potrzebna_do_rekrutacji_nowej_jednostki: int = 1

koszt_ekspansji:int = 5

obrazenia_broni_zelaznej:int = 4
obrazenia_broni_kamiennej:int = 3
obrazenia_broni_drewnianej:int = 2
obrazenia_jednostek_bez_broni:int = 1

obrona_pancerza_zelaznego:int = 4
obrona_pancerza_kamiennego:int = 3
obrona_pancerza_drewnianego:int = 2
obrona_jednostek_bez_pancerza:int = 1

class Panstwo:
    def __init__(
        self, nazwa: str, stolica_x: int, stolica_y: int, agresja: float, kolor: tuple[int, int, int]
    ):
        self.nazwa = nazwa
        self.kolor = kolor
        self.agresja = agresja
        self.typ = "atk" if agresja > 0.5 else "def"
        self.terytorium: set[tuple[int, int]] = {(stolica_x, stolica_y)}
        self.zasoby: dict[str, int] = {
            "drewno": drewno_na_start,
            "kamien": kamien_na_start,
            "zelazo": zelazo_na_start,
            "jedzenie": jedzenie_na_start,
            "jednostki": jednostki_na_start,
        }
        self.wyposazenie: dict[str, int] = {
            "drewniana_bron": 0,
            "drewniany_pancerz": 0,
            
            "kamienna_bron": 0,
            "kamienny_pancerz": 0,
            
            "zelazna_bron": 0,
            "zelazny_pancerz": 0,
        }
        self.statystyki: dict[str, int] = {
            "atak": 0,
            "obrona": 0,
        }

    def przydziel_jednostki(self, grid_size: int, zajete_pola: set[tuple[int, int]], grid: list[list[str]]):

        koszt = koszt_ekspansji + len(self.terytorium)
        #tworzenie jednostek tak aby ich maksymalna liczba nie przekraczala ilosci wolnych pol * agresja
        while True:
            if self.zasoby["jednostki"] < math.ceil(len(self.terytorium)*(self.agresja+1)):
                if self.zasoby["drewno"] >= ilosc_drewna_potrzebna_do_rekrutacji_nowej_jednostki:
                    self.zasoby["drewno"] -= ilosc_drewna_potrzebna_do_rekrutacji_nowej_jednostki
                    self.zasoby["jednostki"] += 1
                else:
                    break
            else:
                break

        temp_jednostki = self.zasoby["jednostki"]

        #zdobywanie jedzenie tak aby jednostki nie ginely z jego braku
        if self.zasoby["jedzenie"] < self.zasoby["jednostki"]:
            if any(grid[y][x] == "J" for x, y in self.terytorium):
                ilosc_jednostek_potrzebnych_do_zdobycia_jedzenia = math.ceil((self.zasoby["jednostki"] - self.zasoby["jedzenie"])/ilosc_jedzenia_z_pola)
                for jednostki in range(ilosc_jednostek_potrzebnych_do_zdobycia_jedzenia):
                    if temp_jednostki > 0:
                        self.zasoby["jedzenie"] += ilosc_jedzenia_z_pola
                        temp_jednostki -= 1
                    else:
                        break

        #zdobywanie nowych terenow
        #przeznaczone na to bedzie taki proecnt jednostek jaki wynosi agresja
        #aby panstwa z zerowa lub bardzo niska agresja nie blokoway sie wykorzystana zostanie funkcja max
        #ktora zawsze przeznaczy przynajmniej 10% jednostek na ekspansje
        ilosc_jednostek_przeznaczonych_na_ekspancje = math.ceil(temp_jednostki * max(0.1 ,self.agresja))
        for jednostki in range(ilosc_jednostek_przeznaczonych_na_ekspancje):
            if self.zasoby["drewno"] >= koszt and temp_jednostki > 0:
                self.ekspansja(grid_size, zajete_pola, koszt)
                temp_jednostki -= 1
                koszt = koszt_ekspansji + len(self.terytorium)
            else:
                break

        #zdobywanie zasobow z wykorzystaniem pozostalych jednostek
        while temp_jednostki > 0:
            zebrano_cos = False
            if min(self.zasoby["drewno"],self.zasoby["kamien"],self.zasoby["zelazo"]) == self.zasoby["zelazo"] and any(grid[y][x] == "Z" for x, y in self.terytorium) and self.zasoby["kamien"] > 0:
                self.zasoby["kamien"] -= 1
                self.zasoby["zelazo"] += 1
                temp_jednostki -= 1
                zebrano_cos = True
            elif min(self.zasoby["drewno"],self.zasoby["kamien"]) == self.zasoby["kamien"] and any(grid[y][x] == "K" for x, y in self.terytorium) and self.zasoby["drewno"] > 0:
                self.zasoby["drewno"] -= 1
                self.zasoby["kamien"] += 1
                temp_jednostki -= 1
                zebrano_cos = True
            elif any(grid[y][x] == "D" for x, y in self.terytorium):
                self.zasoby["drewno"] += 1
                temp_jednostki -= 1
                zebrano_cos = True
            if zebrano_cos:
                continue
            else:
                break

    def utrzymanie_jednostek(self):
        if self.zasoby["jedzenie"] >= self.zasoby["jednostki"]:
            self.zasoby["jedzenie"] -= self.zasoby["jednostki"]
        else:
            self.zasoby["jednostki"] -= self.zasoby["jedzenie"]
            self.zasoby["jedzenie"] = 0

        if self.zasoby["jednostki"] < 0:
            self.zasoby["jednostki"] = 0

    def tworzenie_wyposazenia(self, kategoria: str):
        if self.wyposazenie[f"zelazn{kategoria}"] < self.zasoby["jednostki"]:
            if self.zasoby["zelazo"] > 0:
                self.zasoby["zelazo"] -= 1
                self.wyposazenie[f"zelazn{kategoria}"] += 1

            elif self.wyposazenie[f"kamienn{kategoria}"] > 1:
                self.wyposazenie[f"kamienn{kategoria}"] -= 2
                self.wyposazenie[f"zelazn{kategoria}"] += 1

        if self.wyposazenie[f"kamienn{kategoria}"] < self.zasoby["jednostki"] - self.wyposazenie[f"zelazn{kategoria}"]:
            if self.zasoby["kamien"] > 0:
                self.zasoby["kamien"] -= 1
                self.wyposazenie[f"kamienn{kategoria}"] += 1

            elif self.wyposazenie[f"drewnian{kategoria}"] > 1:
                self.wyposazenie[f"drewnian{kategoria}"] -= 2
                self.wyposazenie[f"kamienn{kategoria}"] += 1

        if self.wyposazenie[f"drewnian{kategoria}"] < self.zasoby["jednostki"] - self.wyposazenie[f"zelazn{kategoria}"] - self.wyposazenie[f"kamienn{kategoria}"]:
            if self.zasoby["drewno"] > 0:
                self.zasoby["drewno"] -= 1
                self.wyposazenie[f"drewnian{kategoria}"] += 1

    def produkcja(self):
        if self.typ == "atk":
            self.tworzenie_wyposazenia("a_bron")
            self.tworzenie_wyposazenia("y_pancerz")
        else:
            self.tworzenie_wyposazenia("y_pancerz")
            self.tworzenie_wyposazenia("a_bron")

    def aktualizacja_statystyk(self):
        if self.typ == "atk":
            modyfikator_atk = 2
            modyfikator_def = 1
        else:
            modyfikator_atk = 1
            modyfikator_def = 2
            
        zelazna_bron = min(self.wyposazenie["zelazna_bron"], self.zasoby["jednostki"])
        kamienna_bron = min(self.wyposazenie["kamienna_bron"], max(0, self.zasoby["jednostki"] - zelazna_bron))
        drewniana_bron = min(self.wyposazenie["drewniana_bron"], max(0,self.zasoby["jednostki"] - zelazna_bron - kamienna_bron))
        ludzie_bron = min(self.zasoby["jednostki"], max(0,self.zasoby["jednostki"] - zelazna_bron - kamienna_bron - drewniana_bron))

        zelazny_pancerz = min(self.wyposazenie["zelazny_pancerz"], self.zasoby["jednostki"])
        kamienny_pancerz = min(self.wyposazenie["kamienny_pancerz"],max(0, self.zasoby["jednostki"] - zelazny_pancerz),)
        drewniany_pancerz = min(self.wyposazenie["drewniany_pancerz"],max(0,self.zasoby["jednostki"] - zelazny_pancerz - kamienny_pancerz))
        ludzie_pancerz = min(self.zasoby["jednostki"],max(0,self.zasoby["jednostki"] - zelazny_pancerz - kamienny_pancerz - drewniany_pancerz))

        self.statystyki["atak"] = (zelazna_bron*obrazenia_broni_zelaznej+kamienna_bron*obrazenia_broni_kamiennej+drewniana_bron*obrazenia_broni_drewnianej+ludzie_bron*obrazenia_jednostek_bez_broni)*modyfikator_atk
        self.statystyki["obrona"] = (zelazny_pancerz*obrona_pancerza_zelaznego+kamienny_pancerz*obrona_pancerza_kamiennego+drewniany_pancerz*obrona_pancerza_drewnianego+ludzie_pancerz*obrona_jednostek_bez_pancerza)*modyfikator_def
        
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

    def ekspansja(self, grid_size: int, zajete_pola: set[tuple[int, int]], koszt):
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
            self.zasoby["drewno"] -= koszt