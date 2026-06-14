import math
from silnik.silnik_panstwo import Panstwo

class PanstwoAgresywne(Panstwo):
    def __init__(
            self,
            nazwa: str,
            stolica_x: int,
            stolica_y: int,
            agresja: float,
            kolor: tuple[int, int, int],
            config: dict
    ):
        super().__init__(nazwa,stolica_x,stolica_y,agresja,kolor,config)
        self.typ="atk"





    def przydziel_jednostki(
       self, grid_size: int, zajete_pola: dict[tuple[int, int]], grid: list[list[str]]
    ):
       koszt =self.koszt_ekspansji + len(self.terytorium)

          # tworzenie jednostek tak aby ich maksymalna liczba nie przekraczala ilosci wolnych pol * agresja
       while True:
           if self.zasoby.get_jednostki() < math.ceil(
               len(self.terytorium) * (self.agresja + 1)
           ):
               if (
                   self.zasoby.get_drewno()
                   >= self.ilosc_drewna_rekrutacja
               ):
                   self.zasoby.zmien_drewno(-self.ilosc_drewna_rekrutacja)
                   self.zasoby.zmien_jednostki(1)
               else:
                   break
           else:
               break

       temp_jednostki = self.zasoby.get_jednostki()

          # zdobywanie jedzenie tak aby jednostki nie ginely z jego braku
       if self.zasoby.get_jedzenie() < self.zasoby.get_jednostki():
               ma_zyzne_pole = any(grid[y][x] == "J" for x, y in self.terytorium)
               wydajnosc = self.ilosc_jedzenia_z_pola if ma_zyzne_pole else 1
               ilosc_jednostek_potrzebnych_do_zdobycia_jedzenia = math.ceil(
                   (self.zasoby.get_jednostki() - self.zasoby.get_jedzenie())
                   / wydajnosc
               )
               for jednostki in range(
                   ilosc_jednostek_potrzebnych_do_zdobycia_jedzenia
               ):
                   if temp_jednostki > 0:
                       self.zasoby.zmien_jedzenie(self.ilosc_jedzenia_z_pola)
                       temp_jednostki -= 1
                   else:
                       break

          # zdobywanie nowych terenow
          # przeznaczone na to bedzie taki proecnt jednostek jaki wynosi agresja
          # aby panstwa z zerowa lub bardzo niska agresja nie blokoway sie wykorzystana zostanie funkcja max
          # ktora zawsze przeznaczy przynajmniej 10% jednostek na ekspansje

       ilosc_jednostek_przeznaczonych_na_ekspancje = math.ceil(
           temp_jednostki * max(0.1, self.agresja)
       )
       for jednostki in range(ilosc_jednostek_przeznaczonych_na_ekspancje):
           if self.zasoby.get_drewno() >= koszt and temp_jednostki > 0:
               self.ekspansja(grid_size, zajete_pola, koszt)
               temp_jednostki -= 1
               koszt = self.koszt_ekspansji + len(self.terytorium)
           else:
               break

          # zdobywanie zasobow z wykorzystaniem pozostalych jednostek
       while temp_jednostki > 0:
           zebrano_cos = False
           if (
               min(self.zasoby.get_drewno(), self.zasoby.get_kamien(), self.zasoby.get_zelazo())
               == self.zasoby.get_zelazo()
               and any(grid[y][x] == "Z" for x, y in self.terytorium)
               and self.zasoby.get_kamien() > 0
           ):
               self.zasoby.zmien_kamien(-1)
               self.zasoby.zmien_zelazo(1)
               temp_jednostki -= 1
               zebrano_cos = True
           elif (
               min(self.zasoby.get_drewno(), self.zasoby.get_kamien()) == self.zasoby.get_kamien()
               and any(grid[y][x] == "K" for x, y in self.terytorium)
               and self.zasoby.get_drewno() > 0
           ):
               self.zasoby.zmien_drewno(-1)
               self.zasoby.zmien_kamien(1)
               temp_jednostki -= 1
               zebrano_cos = True
           elif any(grid[y][x] == "D" for x, y in self.terytorium):
               self.zasoby.zmien_drewno(1)
               temp_jednostki -= 1
               zebrano_cos = True
           elif len(self.terytorium) >0:
               self.zasoby.zmien_drewno(1)
               temp_jednostki -=1
               zebrano_cos = True
           if zebrano_cos:
               continue
           else:
               break


class PanstwoDefensywne(Panstwo):

    def __init__(
            self,
            nazwa: str,
            stolica_x: int,
            stolica_y: int,
            agresja: float,
            kolor: tuple[int, int, int],
            config: dict
    ):
        super().__init__(nazwa,stolica_x,stolica_y,agresja,kolor,config)
        self.typ="def"





    def przydziel_jednostki(
       self, grid_size: int, zajete_pola: dict[tuple[int, int], 'Panstwo'], grid: list[list[str]]
    ):
       koszt =self.koszt_ekspansji + len(self.terytorium)

          # tworzenie jednostek tak aby ich maksymalna liczba nie przekraczala ilosci wolnych pol * agresja
       while True:
           if self.zasoby.get_jednostki() < math.ceil(
               len(self.terytorium) * (self.agresja + 1)
           ):
               if (
                   self.zasoby.get_drewno()
                   >= self.ilosc_drewna_rekrutacja
               ):
                   self.zasoby.zmien_drewno(-self.ilosc_drewna_rekrutacja)
                   self.zasoby.zmien_jednostki(1)
               else:
                   break
           else:
               break

       temp_jednostki = self.zasoby.get_jednostki()

          # zdobywanie jedzenie tak aby jednostki nie ginely z jego braku
       if self.zasoby.get_jedzenie() < self.zasoby.get_jednostki():
            if any(grid[y][x] == "J" for x, y in self.terytorium):
               ilosc_jednostek_potrzebnych_do_zdobycia_jedzenia = math.ceil(
                   (self.zasoby.get_jednostki() - self.zasoby.get_jedzenie())
                   / self.ilosc_jedzenia_z_pola
               )
               for jednostki in range(
                   ilosc_jednostek_potrzebnych_do_zdobycia_jedzenia
               ):
                   if temp_jednostki > 0:
                       self.zasoby.zmien_jedzenie(self.ilosc_jedzenia_z_pola)
                       temp_jednostki -= 1
                   else:
                       break

          # zdobywanie nowych terenow
          # przeznaczone na to bedzie taki proecnt jednostek jaki wynosi agresja
          # aby panstwa z zerowa lub bardzo niska agresja nie blokoway sie wykorzystana zostanie funkcja max
          # ktora zawsze przeznaczy przynajmniej 10% jednostek na ekspansje

       ilosc_jednostek_przeznaczonych_na_ekspancje = math.ceil(
           temp_jednostki * max(0.1, self.agresja)
       )
       for jednostki in range(ilosc_jednostek_przeznaczonych_na_ekspancje):
           if self.zasoby.get_drewno() >= koszt and temp_jednostki > 0:
               self.ekspansja(grid_size, zajete_pola, koszt)
               temp_jednostki -= 1
               koszt = self.koszt_ekspansji + len(self.terytorium)
           else:
               break

          # zdobywanie zasobow z wykorzystaniem pozostalych jednostek
       while temp_jednostki > 0:
           zebrano_cos = False
           if (
               min(self.zasoby.get_drewno(), self.zasoby.get_kamien(), self.zasoby.get_zelazo())
               == self.zasoby.get_zelazo()
               and any(grid[y][x] == "Z" for x, y in self.terytorium)
               and self.zasoby.get_kamien() > 0
           ):
               self.zasoby.zmien_kamien(-1)
               self.zasoby.zmien_zelazo(1)
               temp_jednostki -= 1
               zebrano_cos = True
           elif (
               min(self.zasoby.get_drewno(), self.zasoby.get_kamien()) == self.zasoby.get_kamien()
               and any(grid[y][x] == "K" for x, y in self.terytorium)
               and self.zasoby.get_drewno() > 0
           ):
               self.zasoby.zmien_drewno(-1)
               self.zasoby.zmien_kamien(1)
               temp_jednostki -= 1
               zebrano_cos = True
           elif any(grid[y][x] == "D" for x, y in self.terytorium):
               self.zasoby.zmien_drewno(1)
               temp_jednostki -= 1
               zebrano_cos = True
           elif len(self.terytorium) >0:
               self.zasoby.zmien_drewno(1)
               temp_jednostki -=1
               zebrano_cos = True
           if zebrano_cos:
               continue
           else:
               break