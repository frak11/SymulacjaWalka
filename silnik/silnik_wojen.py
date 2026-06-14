import random

from gui.wizualizacja import okno
from silnik.silnik_panstwo import Panstwo


class SystemWojen:
    def sprawdz_wojne(panstwo_atakujace, grid_size: int, zajete_pola: dict[tuple[int, int], 'Panstwo'], lista_panstw: list[Panstwo]):
        mozliwe_pola: set[tuple[int, int]] = set()
        sasiedzi=[(0,-1),(-1,0),(0,1),(1,0)]
        tury =okno.instancja.numer_tury
    
        for x, y in panstwo_atakujace.terytorium:
            for dx, dy in sasiedzi:
                nx, ny = x+dx, y+dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    if (nx,ny) in zajete_pola and (nx,ny) not in panstwo_atakujace.terytorium:
                        mozliwe_pola.add((nx, ny))
        if mozliwe_pola:
            losowanie_pola = random.choice(list(mozliwe_pola))
            panstwo_broniace = zajete_pola[losowanie_pola]
            chance = random.random()
            atk = panstwo_atakujace.statystyki["atak"]
            obr = panstwo_broniace.statystyki["obrona"]
            if panstwo_broniace.agresja <= panstwo_atakujace.agresja:
                okno.instancja.dodaj_wiadomosc(f"{panstwo_atakujace.nazwa} (Atk:{atk}) atakuje {panstwo_broniace.nazwa} (Def:{obr}", tura =tury)
                if chance < panstwo_atakujace.agresja:
                    okno.instancja.dodaj_wiadomosc(f"szansa < agresja")
                    while True:
                        panstwo_broniace.statystyki["obrona"] -= panstwo_atakujace.statystyki["atak"]
                        panstwo_atakujace.statystyki["obrona"] -= panstwo_broniace.statystyki["atak"]
                        if panstwo_broniace.statystyki["obrona"] < 0 and panstwo_atakujace.statystyki["obrona"] < 0:
                            # oba panstwa zniszczyly sie w tym samym czasie
                            lista_panstw.remove(panstwo_atakujace)
                            lista_panstw.remove(panstwo_broniace)
                            okno.instancja.dodaj_wiadomosc(f"{panstwo_broniace.nazwa} i {panstwo_atakujace.nazwa} zniszczyły się nawzajem", tura =tury)
                            for pole in panstwo_broniace.terytorium:
                                del zajete_pola[pole]
                            for pole in panstwo_atakujace.terytorium:
                                del zajete_pola[pole]
                            break
                        elif panstwo_broniace.statystyki["obrona"] < 0:
                            okno.instancja.dodaj_wiadomosc(f"{panstwo_broniace.nazwa} przegrywa", tura =tury)
                            # panstwo atakowane przegralo
                            for pole in panstwo_broniace.terytorium:
                                zajete_pola[pole] = panstwo_atakujace
                            panstwo_atakujace.terytorium.update(panstwo_broniace.terytorium)
                            lista_panstw.remove(panstwo_broniace)
                            break
                        elif panstwo_atakujace.statystyki["obrona"] < 0:
                            okno.instancja.dodaj_wiadomosc(f"{panstwo_atakujace.nazwa} + przegrywa", tura =tury)
                            # panstwo atakujace przegralo
                            for pole in panstwo_atakujace.terytorium:
                                zajete_pola[pole] = panstwo_broniace
                            panstwo_broniace.terytorium.update(panstwo_atakujace.terytorium)
                            lista_panstw.remove(panstwo_atakujace)
                            break
                else:
                    okno.instancja.dodaj_wiadomosc(f"za mala szansa, nie ma wojny", tura =tury)
