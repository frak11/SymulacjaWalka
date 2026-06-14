import sys
import pygame


kolor_tlo = (30, 30, 30)
kolor_panelu = (0, 0, 0)
kolor_siatka = (50, 50, 50)
kolor_ziemia = (34, 139, 34)
kolor_drewno = (139, 69, 19)
kolor_kamien = (128, 128, 128)
kolor_zelazo = (192, 192, 192)
kolor_jedzenie = (245,222,179)


class okno:
    def __init__(self, grid, lista_panstw, rozmiar_siatki, zajete_pola, tura):
        self.czciona = pygame.font.SysFont("Arial", 18)
        self.czcionka_naglowek = pygame.font.SysFont("Arial", 24, bold=True)
        self.grid = grid
        self.gridSize = len(self.grid)
        self.lista_panstw = lista_panstw
        self.rozmiar_siatki = rozmiar_siatki
        self.zajete_pola = zajete_pola
        self.wykonaj_ture = tura

        self.kafelek: int = 20
        self.pixele = self.gridSize * self.kafelek
        self.panel_boczny = 600

        self.screen = pygame.display.set_mode(
            (self.pixele + self.panel_boczny, self.pixele)
        )
        pygame.display.set_caption("2D mapa")
        self.clock = pygame.time.Clock()
        self.running = True
        self.numer_tury= 0

        self.logi =[]
        okno.instancja = self

    def dodaj_wiadomosc(self, tekst: str, tura: int =None):
        if tura is not None:
            pelny_tekst = f"[{tura}] {tekst}"
        else:
            pelny_tekst = tekst
        self.logi.append(pelny_tekst)
        if len(self.logi)>15:
            self.logi.pop(0)


    def run(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.numer_tury += 1
                        self.wykonaj_ture()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for tury in range(10):
                        self.numer_tury += 1
                        self.wykonaj_ture()

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
                    elif rodzaj_pola == "J":
                        kolor = kolor_jedzenie
                    else:
                        kolor = kolor_ziemia

                    pygame.draw.rect(self.screen, kolor, kwadrat)
                    pygame.draw.rect(self.screen, kolor_siatka, kwadrat, 1)
                    for panstwo in self.lista_panstw:
                        if (x, y) in panstwo.terytorium:
                            margines = self.kafelek*0.2
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
            tekst_tura=self.czcionka_naglowek.render(f"Tura: {self.numer_tury}", True, (255, 255, 255))
            self.screen.blit(tekst_tura, (self.pixele+ 20, 20))

            pozycja_wyswietlenia =80

            for panstwo in self.lista_panstw:
                kwadrat = pygame.Rect(self.pixele +20, pozycja_wyswietlenia+ 5, 15,15)
                pygame.draw.rect(self.screen, panstwo.kolor, kwadrat)
                tekst_nazwa = self.czcionka_naglowek.render(panstwo.nazwa, True, panstwo.kolor)
                self.screen.blit(tekst_nazwa, (self.pixele+ 45, pozycja_wyswietlenia))
                pozycja_wyswietlenia += 30

                surowce_str = (
                    f"Terytorium: {len(panstwo.terytorium)} |"
                    f"Drewno: {panstwo.zasoby.get_drewno()} |"
                    f"Kamien: {panstwo.zasoby.get_kamien()} |"
                    f"Żelazo: {panstwo.zasoby.get_zelazo()} |"
                    f"Jedzenie: {panstwo.zasoby.get_jedzenie()} |"
                    f"Jednostki: {panstwo.zasoby.get_jednostki()} |"
                )
                tekt_staty =self.czciona.render(surowce_str, True, panstwo.kolor)
                self.screen.blit(tekt_staty, (self.pixele+ 20, pozycja_wyswietlenia))
                pozycja_wyswietlenia += 20

                zel_b= panstwo.wyposazenie.get("zelazna_bron")
                kam_b = panstwo.wyposazenie.get("kamienna_bron")
                dre_b = panstwo.wyposazenie.get("drewniana_bron")
                zel_p = panstwo.wyposazenie.get("zelazny_pancerz")
                kam_p= panstwo.wyposazenie.get("kamienny_pancerz")
                dre_p=panstwo.wyposazenie.get("drewniany_pancerz")

                sila_str =(
                    f"Siła: ATK: {panstwo.statystyki['atak']} | DEF: {panstwo.statystyki['obrona']} | ")
                tekst_sila = self.czciona.render(sila_str, True, panstwo.kolor)
                self.screen.blit(tekst_sila, (self.pixele + 20, pozycja_wyswietlenia))
                pozycja_wyswietlenia += 20
                uzbrojenie_str =(
                f"Broń: Żelazna: {zel_b} | Kamienna: {kam_b} | Drewniana: {dre_b} |"
                )
                tekst_bron = self.czciona.render(uzbrojenie_str, True, panstwo.kolor)
                self.screen.blit(tekst_bron, (self.pixele+ 20, pozycja_wyswietlenia))
                pozycja_wyswietlenia += 20
                pan_str = (
                f"Pancerz: Żelazny: {zel_p} | Kamienny: {kam_p} | Drewniany: {dre_p} |")
                tekt_pan=self.czciona.render(pan_str, True, panstwo.kolor)
                self.screen.blit(tekt_pan, (self.pixele+ 20, pozycja_wyswietlenia))
                pozycja_wyswietlenia += 30




            pozycja_wyswietlenia += 30
            tekst_naglowek_logi = self.czcionka_naglowek.render("Wydarzenia: ",True, (255, 215, 0))
            self.screen.blit(tekst_naglowek_logi, (self.pixele+ 20, pozycja_wyswietlenia))
            pozycja_wyswietlenia += 35

            for tekst in self.logi:
                tekst_render =self.czciona.render(tekst, True,(220, 220, 220))
                self.screen.blit(tekst_render, (self.pixele+ 20, pozycja_wyswietlenia))
                pozycja_wyswietlenia += 22


            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()
