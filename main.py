from pygame.examples import grid

from silnik.silnik_symulacji import generuj_mape
from gui.wizualizacja import okno

def main():
 seed =123
 spawn_rate=2
 rozmiar_siatki =40

 mapa = generuj_mape(gridSize = rozmiar_siatki, spawnRate = spawn_rate, seed = seed)
 ekran=okno(grid=mapa)
 ekran.run()
main()
