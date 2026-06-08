from silnik.silnik_symulacji import generuj_mape
from gui.wizualizacja import okno
from silnik.silnik_panstwo import Panstwo

def main():

    seed = 167324
    spawn_rate = 7
    rozmiar_siatki = 40
    zajete_pola: set[tuple[int, int]] = set()

    mapa = generuj_mape(grid_size=rozmiar_siatki, spawn_rate=spawn_rate, seed=seed)

    panstwo1 = Panstwo(
        nazwa="imperium",
        stolica_x=0,
        stolica_y=0,
        kolor=(255,0,0),
        agresja=1
    )

    panstwo2 = Panstwo(
        nazwa="republika",
        stolica_x=rozmiar_siatki -1,
        stolica_y=rozmiar_siatki -1,
        kolor=(0,0,255),
        agresja=0
    )

    panstwo3 = Panstwo(
        nazwa="p3",
        stolica_x=0,
        stolica_y=rozmiar_siatki - 1,
        kolor=(0, 255, 0),
        agresja=0.5
    )

    panstwo4 = Panstwo(
        nazwa="p4",
        stolica_x=rozmiar_siatki - 1,
        stolica_y=0,
        kolor=(255, 0, 255),
        agresja=0.3,
    )

    lista_panstw = [panstwo1, panstwo2, panstwo3, panstwo4]
    for p in lista_panstw:
        for pole in p.terytorium:
            zajete_pola.add(pole)

    def wykonaj_ture():
        for p in lista_panstw:
            p.przydziel_jednostki(rozmiar_siatki, zajete_pola, mapa)
            p.utrzymanie_jednostek()
            p.produkcja()
            p.aktualizacja_statystyk()

    ekran = okno(
        grid=mapa,
        lista_panstw=lista_panstw,
        rozmiar_siatki=rozmiar_siatki,
        zajete_pola=zajete_pola,
        tura = wykonaj_ture
    )
    ekran.run()

main()
