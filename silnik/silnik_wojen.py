import random

from gui.wizualizacja import Okno
from silnik.silnik_panstwo import Panstwo


class SystemWojen:
    trwajace_wojny: dict['Panstwo', list[tuple[int, int]]] = dict()

    @classmethod
    def sprawdz_wojne(cls, panstwo_atakujace, grid_size: int, zajete_pola: dict[tuple[int, int], 'Panstwo'], lista_panstw: list[Panstwo]):
        mozliwe_pola: set[tuple[int, int]] = set()
        sasiedzi=[(0,-1),(-1,0),(0,1),(1,0)]
        tury = Okno.instancja.numer_tury
    
        for x, y in panstwo_atakujace.terytorium:
            for dx, dy in sasiedzi:
                nx, ny = x+dx, y+dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    if (nx,ny) in zajete_pola and (nx,ny) not in panstwo_atakujace.terytorium:
                        if zajete_pola[(nx,ny)] in lista_panstw:
                            mozliwe_pola.add((nx, ny))
        if mozliwe_pola:
            losowanie_pola = random.choice(list(mozliwe_pola))
            panstwo_broniace = zajete_pola[losowanie_pola]
            chance = random.random()
            atk = panstwo_atakujace.statystyki["atak"]
            obr = panstwo_broniace.statystyki["obrona"]
            if panstwo_broniace.agresja <= panstwo_atakujace.agresja:
                Okno.instancja.dodaj_wiadomosc(f"{panstwo_atakujace.nazwa} (Atk:{atk}) atakuje {panstwo_broniace.nazwa} (Def:{obr}", tura =tury)
                if chance < panstwo_atakujace.agresja:
                    Okno.instancja.dodaj_wiadomosc(f"szansa < agresja")
                    while True:
                        panstwo_broniace.statystyki["obrona"] -= panstwo_atakujace.statystyki["atak"]
                        panstwo_atakujace.statystyki["obrona"] -= panstwo_broniace.statystyki["atak"]
                        if panstwo_broniace.statystyki["obrona"] < 0 and panstwo_atakujace.statystyki["obrona"] < 0:
                            # oba panstwa zniszczyly sie w tym samym czasie
                            pomieszane_pola = list(panstwo_broniace.terytorium) + list(panstwo_atakujace.terytorium)
                            random.shuffle(pomieszane_pola)
                            cls.trwajace_wojny[None] = cls.trwajace_wojny.get(None, []) + pomieszane_pola
                            for pole in pomieszane_pola:
                                if pole in zajete_pola:
                                    del zajete_pola[pole]
                            panstwo_broniace.terytorium.clear()
                            panstwo_atakujace.terytorium.clear()
                            lista_panstw.remove(panstwo_atakujace)
                            lista_panstw.remove(panstwo_broniace)
                            Okno.instancja.dodaj_wiadomosc(f"{panstwo_broniace.nazwa} i {panstwo_atakujace.nazwa} zniszczyły się nawzajem", tura =tury)
                            return
                        elif panstwo_broniace.statystyki["obrona"] < 0:
                            Okno.instancja.dodaj_wiadomosc(f"{panstwo_broniace.nazwa} przegrywa", tura =tury)
                            # panstwo broniace przegralo
                            cls.trwajace_wojny[panstwo_atakujace] = list(panstwo_broniace.terytorium)
                            for pole in panstwo_broniace.terytorium:
                                if pole in zajete_pola:
                                    del zajete_pola[pole]

                            panstwo_broniace.terytorium.clear()
                            lista_panstw.remove(panstwo_broniace)
                            return
                        elif panstwo_atakujace.statystyki["obrona"] < 0:
                            Okno.instancja.dodaj_wiadomosc(f"{panstwo_atakujace.nazwa} + przegrywa", tura =tury)
                            # panstwo atakujace przegralo
                            cls.trwajace_wojny[panstwo_broniace] = list(panstwo_atakujace.terytorium)
                            for pole in panstwo_atakujace.terytorium:
                                if pole in zajete_pola:
                                    del zajete_pola[pole]
                            panstwo_atakujace.terytorium.clear()
                            lista_panstw.remove(panstwo_atakujace)
                            return
                else:
                    Okno.instancja.dodaj_wiadomosc(f"za mala szansa, nie ma wojny", tura =tury)

    @classmethod
    def przejmij_pola(cls, zajete_pola, lista_panstw):
        for zwyciezca, przegrany_terytorium in list(cls.trwajace_wojny.items()):

            if zwyciezca is not None and zwyciezca not in lista_panstw:
                    del cls.trwajace_wojny[zwyciezca]
                    continue

            for x in range(5):
                if przegrany_terytorium:
                    pole = przegrany_terytorium.pop()
                    if zwyciezca is not None:
                        zwyciezca.terytorium.add(pole)
                        zajete_pola[pole] = zwyciezca
                    else:
                        if pole in zajete_pola:
                            del zajete_pola[pole]
                    if not przegrany_terytorium:
                        del cls.trwajace_wojny[zwyciezca]
                        break