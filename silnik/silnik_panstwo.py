import math
import random
from silnik.zasoby import Zasoby
from silnik.wyposazenie import Wyposazenie

drewno_na_start: int = 60
kamien_na_start: int = 0
zelazo_na_start: int = 0
jedzenie_na_start: int = 20
jednostki_na_start: int = 3
ilosc_jedzenia_z_pola: int = 3
ilosc_drewna_potrzebna_do_rekrutacji_nowej_jednostki: int = 1
koszt_ekspansji: int = 5

obrazenia_broni_zelaznej: int = 4
obrazenia_broni_kamiennej: int = 3
obrazenia_broni_drewnianej: int = 2
obrazenia_jednostek_bez_broni: int = 1

obrona_pancerza_zelaznego: int = 4
obrona_pancerza_kamiennego: int = 3
obrona_pancerza_drewnianego: int = 2
obrona_jednostek_bez_pancerza: int = 1


class Panstwo:
    def __init__(
        self,
        nazwa: str,
        stolica_x: int,
        stolica_y: int,
        agresja: float,
        kolor: tuple[int, int, int],
    ):
        self.nazwa = nazwa
        self.kolor = kolor
        self.agresja = agresja
        self.terytorium: set[tuple[int, int]] = {(stolica_x, stolica_y)}
        self.zasoby = Zasoby(drewno_na_start, kamien_na_start,zelazo_na_start,jedzenie_na_start,jednostki_na_start)
        self.wyposazenie =Wyposazenie()

        self.statystyki: dict[str, int] = {
            "atak": 0,
            "obrona": 0,
        }
        self.typ ="def"



    def utrzymanie_jednostek(self):
        if self.zasoby.get_jedzenie() >= self.zasoby.get_jednostki():
            self.zasoby.zmien_jedzenie(-self.zasoby.get_jednostki())
        else:
            ile_umrze = self.zasoby.get_jednostki() - self.zasoby.get_jedzenie()
            self.zasoby.zmien_jednostki(-ile_umrze)
            self.zasoby.ustaw_jedzenie(0)

    def tworzenie_wyposazenia(self, kategoria: str):
        if self.wyposazenie.get(f"zelazn{kategoria}") < self.zasoby.get_jednostki():
            if self.zasoby.get_zelazo() > 0:
                self.zasoby.zmien_zelazo(-1)
                self.wyposazenie.zmien(f"zelazn{kategoria}",1)

            elif self.wyposazenie.get(f"kamienn{kategoria}") > 1:
                self.wyposazenie.zmien(f"kamienn{kategoria}",-2)
                self.wyposazenie.zmien(f"zelazn{kategoria}",1)

        if self.wyposazenie.get(f"kamienn{kategoria}") <self.zasoby.get_jednostki() - self.wyposazenie.get(f"zelazn{kategoria}"):
            if self.zasoby.get_kamien() > 0:
                self.zasoby.zmien_kamien(-1)
                self.wyposazenie.zmien(f"kamienn{kategoria}",1)

            elif self.wyposazenie.get(f"drewnian{kategoria}") > 1:
                self.wyposazenie.zmien(f"drewnian{kategoria}",-2)
                self.wyposazenie.zmien(f"kamienn{kategoria}",1)

        if (
            self.wyposazenie.get(f"drewnian{kategoria}")
            < self.zasoby.get_jednostki()
            - self.wyposazenie.get(f"zelazn{kategoria}")
            - self.wyposazenie.get(f"kamienn{kategoria}")
        ):
            if self.zasoby.get_drewno() > 0:
                self.zasoby.zmien_drewno(-1)
                self.wyposazenie.zmien(f"drewnian{kategoria}",1)

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

        zelazna_bron = min(self.wyposazenie.get("zelazna_bron"), self.zasoby.get_jednostki())
        kamienna_bron = min(
            self.wyposazenie.get("kamienna_bron"),
            max(0, self.zasoby.get_jednostki() - zelazna_bron),
        )
        drewniana_bron = min(
            self.wyposazenie.get("drewniana_bron"),
            max(0, self.zasoby.get_jednostki() - zelazna_bron - kamienna_bron),
        )
        ludzie_bron = min(
            self.zasoby.get_jednostki(),
            max(
                0,
                self.zasoby.get_jednostki()
                - zelazna_bron
                - kamienna_bron
                - drewniana_bron,
            ),
        )

        zelazny_pancerz = min(
            self.wyposazenie.get("zelazny_pancerz"), self.zasoby.get_jednostki()
        )
        kamienny_pancerz = min(
            self.wyposazenie.get("kamienny_pancerz"),
            max(0, self.zasoby.get_jednostki() - zelazny_pancerz),
        )
        drewniany_pancerz = min(
            self.wyposazenie.get("drewniany_pancerz"),
            max(0, self.zasoby.get_jednostki() - zelazny_pancerz - kamienny_pancerz),
        )
        ludzie_pancerz = min(
            self.zasoby.get_jednostki(),
            max(
                0,
                self.zasoby.get_jednostki()
                - zelazny_pancerz
                - kamienny_pancerz
                - drewniany_pancerz,
            ),
        )

        self.statystyki["atak"] = (
            zelazna_bron * obrazenia_broni_zelaznej
            + kamienna_bron * obrazenia_broni_kamiennej
            + drewniana_bron * obrazenia_broni_drewnianej
            + ludzie_bron * obrazenia_jednostek_bez_broni
        ) * modyfikator_atk
        self.statystyki["obrona"] = (
            zelazny_pancerz * obrona_pancerza_zelaznego
            + kamienny_pancerz * obrona_pancerza_kamiennego
            + drewniany_pancerz * obrona_pancerza_drewnianego
            + ludzie_pancerz * obrona_jednostek_bez_pancerza
        ) * modyfikator_def

    def ekspansja(self, grid_size: int, zajete_pola: dict[tuple[int, int], 'Panstwo'], koszt: int):
        mozliwe_pola: set[tuple[int, int]] = set()
        sasiedzi = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        for x, y in self.terytorium:
            for dx, dy in sasiedzi:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    if (nx, ny) not in zajete_pola:
                        mozliwe_pola.add((nx, ny))
        if mozliwe_pola:
            losowanie_pola = random.choice(list(mozliwe_pola))
            self.terytorium.add(losowanie_pola)
            zajete_pola[losowanie_pola] =self
            self.zasoby.zmien_drewno(-koszt)

    def przydziel_jednostki(
        self, grid_size: int, zajete_pola: set[tuple[int, int]], grid: list[list[str]]
    ):
        pass

