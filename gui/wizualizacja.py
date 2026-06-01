import sys
import pygame


kolor_tlo = (30, 30, 30)
kolor_panelu = (0, 0, 0)
kolor_siatka = (50, 50, 50)
kolor_ziemia = (34, 139, 34)
kolor_drewno = (139, 69, 19)
kolor_kamien = (128, 128, 128)
kolor_zelazo = (192, 192, 192)


class okno:
    def __init__(self, grid, lista_panstw,rozmiar_siatki, zajete_pola):
        pygame.init()
        self.grid = grid
        self.gridSize = len(self.grid)
        self.lista_panstw = lista_panstw
        self.rozmiar_siatki = rozmiar_siatki
        self.zajete_pola = zajete_pola

        self.kafelek: int = 20
        self.pixele = self.gridSize * self.kafelek
        self.panel_boczny = 400

        self.screen = pygame.display.set_mode(
            (self.pixele + self.panel_boczny, self.pixele)
        )
        pygame.display.set_caption("2D mapa")
        self.clock = pygame.time.Clock()
        self.running = True
        self.tura= 0


    def run(self):
        d= pygame.time.get_ticks()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            b = pygame.time.get_ticks()

            if b - d > 1000:
                self.tura+=1
                for p in self.lista_panstw:
                    p.zbierz_surowce(self.grid)
                    p.ekspansja(self.gridSize, self.zajete_pola)

                d=b



            self.screen.fill(kolor_tlo)

            for x in range(self.gridSize):
                for y in range(self.gridSize):
                    pozycjax = x * self.kafelek
                    pozycjay = y * self.kafelek

                    kwadrat = pygame.Rect(
                        pozycjax, pozycjay, self.kafelek, self.kafelek
                    )
                    rodzaj_pola = self.grid[y][x]
                    if rodzaj_pola == "D":
                        kolor = kolor_drewno
                    elif rodzaj_pola == "K":
                        kolor = kolor_kamien
                    elif rodzaj_pola == "Z":
                        kolor = kolor_zelazo
                    else:
                        kolor = kolor_ziemia

                    pygame.draw.rect(self.screen, kolor, kwadrat)
                    pygame.draw.rect(self.screen, kolor_siatka, kwadrat, 1)
                    for panstwo in self.lista_panstw:
                        if (x, y) in panstwo.terytorium:
                            margines = 4
                            kwadrat_panstwa = pygame.Rect(
                                pozycjax + margines,
                                pozycjay + margines,
                                self.kafelek - (margines * 2),
                                self.kafelek - (margines * 2),
                            )
                            pygame.draw.rect(self.screen, panstwo.kolor, kwadrat_panstwa)

            obszar_panelu = pygame.Rect(self.pixele, 0, self.panel_boczny, self.pixele)
            pygame.draw.rect(self.screen, kolor_panelu, obszar_panelu)
            pygame.draw.line(
                self.screen,
                kolor_siatka,
                (self.pixele, 0),
                (self.pixele, self.pixele),
                2,
            )

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()
