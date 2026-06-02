import time

from pygame.examples import grid

from silnik.silnik_symulacji import generuj_mape
from gui.wizualizacja import okno
from silnik.silnik_panstwo import Panstwo


def main():
    seed = 1
    spawn_rate = 2
    rozmiar_siatki =40
    liczba_tur =100

    mapa = generuj_mape(gridSize=rozmiar_siatki, spawnRate=spawn_rate, seed=seed)

    zajete_pola: set[tuple[int, int]]=set()
    panstwo1 = Panstwo(
        nazwa="imperium",
        stolica_x=0,
        stolica_y=0,
        kolor=(255,0,0)
    )
    panstwo2 = Panstwo(
        nazwa="republika",
        stolica_x=rozmiar_siatki -1,
        stolica_y=rozmiar_siatki -1,
        kolor=(0,0,255)
    )
    lista_panstw = [panstwo1, panstwo2]
    for p in lista_panstw:
        for pole in p.terytorium:
            zajete_pola.add(pole)

    ekran = okno(grid=mapa,lista_panstw=lista_panstw,rozmiar_siatki=rozmiar_siatki,zajete_pola=zajete_pola)

    for p in lista_panstw:

            p.zbierz_surowce(mapa)
            p.ekspansja(rozmiar_siatki,zajete_pola)


    ekran.run()


main()
