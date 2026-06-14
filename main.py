import pygame
import random
import json
from silnik.silnik_symulacji import generuj_mape
from gui.wizualizacja import okno
from silnik.typy_panstw import PanstwoAgresywne,PanstwoDefensywne
from silnik.silnik_wojen import SystemWojen
from silnik.silnik_panstwo import Panstwo
def wczytaj_konfiguracja(sciezka="konfiguracja.json"):
    with open(sciezka) as json_file:
        return json.load(json_file)
def main():
    config = wczytaj_konfiguracja()
    pygame.init()
    seed =config["seed"]
    random.seed(seed)
    spawn_rate =config["spawn_rate"]
    rozmiar_siatki =config["rozmiar_siatki"]
    losowe_pozycje=config["losowe_pozycje"]
    zajete_pola: dict[tuple[int, int], 'Panstwo'] = dict()

    mapa = generuj_mape(grid_size=rozmiar_siatki, spawn_rate=spawn_rate)


    lista_panstw = []
    for panstwa_data in config["panstwa"]:
        kolor = panstwa_data["kolor"]
        if kolor == "random":
            kolor =(random.randint(100,255),random.randint(100,255),random.randint(100,255))
        else:
            kolor = tuple(kolor)
        if losowe_pozycje:
            while True:
                x = random.randrange(0, rozmiar_siatki-1)
                y = random.randrange(0, rozmiar_siatki-1)
                if(x,y) not in zajete_pola:
                     break
        else:
            x=panstwa_data["stolica_x"]
            y=panstwa_data["stolica_y"]


        if panstwa_data["typ"]== "atk":
            nowe_panstwo =PanstwoAgresywne(panstwa_data["nazwa"],x,y,panstwa_data["agresja"],kolor,config["ustawienia_gry"])
        else:
            nowe_panstwo =PanstwoDefensywne(panstwa_data["nazwa"],x,y,panstwa_data["agresja"],kolor,config["ustawienia_gry"])

        lista_panstw.append(nowe_panstwo)
        zajete_pola[(x,y)] = nowe_panstwo

    def wykonaj_ture():
        for p in lista_panstw:
            p.przydziel_jednostki(rozmiar_siatki, zajete_pola, mapa)
            p.utrzymanie_jednostek()
            p.produkcja()
            p.aktualizacja_statystyk()
        for p in lista_panstw[:]:
            if p in lista_panstw:
                SystemWojen.sprawdz_wojne(p,rozmiar_siatki,zajete_pola,lista_panstw)

    ekran = okno(
        grid=mapa,
        lista_panstw=lista_panstw,
        rozmiar_siatki=rozmiar_siatki,
        zajete_pola=zajete_pola,
        tura = wykonaj_ture
    )
    ekran.run()

main()
