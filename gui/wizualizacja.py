import sys
import pygame

pygame.init()


wysokosc: int = 1200
szerokosc: int = 800
kafelek: int = 20

panel_boczny: int = wysokosc - szerokosc
kolor_tlo = (30, 30, 30)
kolor_panelu = (20, 20, 20)
kolor_siatka = (50, 50, 50)
kolor_ziemia = (34, 139, 34)


class okno:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((wysokosc, szerokosc))
        pygame.display.set_caption("2D mapa")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


            self.screen.fill(kolor_tlo)

            for y in range(szerokosc // kafelek):
                for x in range(szerokosc // kafelek):
                    pozycjax = x * kafelek
                    pozycjay = y * kafelek

                    kwadrat = pygame.Rect(pozycjax, pozycjay, kafelek, kafelek)
                    pygame.draw.rect(self.screen, kolor_ziemia, kwadrat)
                    pygame.draw.rect(self.screen, kolor_siatka, kwadrat, 1)



            obszar_panelu = pygame.Rect(szerokosc, 0, panel_boczny, szerokosc)
            pygame.draw.rect(self.screen, kolor_panelu, obszar_panelu)
            pygame.draw.line(
                self.screen, kolor_siatka, (szerokosc, 0), (szerokosc, szerokosc), 2
            )


            pygame.display.flip()


            self.clock.tick(60)

        pygame.quit()
        sys.exit()



if __name__ == "__main__":
    gra = okno()
    gra.run()