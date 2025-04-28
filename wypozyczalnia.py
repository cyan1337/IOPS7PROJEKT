from datetime import date

class Samochod:
    def __init__(self, id_samochodu, marka, model, cena_za_dzien, dostepny=True):
        self.id_samochodu = id_samochodu
        self.marka = marka
        self.model = model
        self.cena_za_dzien = cena_za_dzien
        self.dostepny = dostepny

class Klient:
    def __init__(self, id_klienta, imie_nazwisko, email):
        self.id_klienta = id_klienta
        self.imie_nazwisko = imie_nazwisko
        self.email = email

class Rezerwacja:
    def __init__(self, id_rezerwacji, klient, samochod, data_startu, data_konca):
        self.id_rezerwacji = id_rezerwacji
        self.klient = klient
        self.samochod = samochod
        self.data_startu = data_startu
        self.data_konca = data_konca
        self.calkowity_koszt = self.oblicz_cene()

    def oblicz_cene(self):
        dni = (self.data_konca - self.data_startu).days
        if dni <= 0:
            raise ValueError("Data końca musi być po dacie startu.")
        return dni * self.samochod.cena_za_dzien

# ------------------------------
# Funkcje aplikacji
# ------------------------------

def dodaj_samochod(lista_samochodow, samochod):
    """Dodaje nowy samochód do listy."""
    lista_samochodow.append(samochod)
    return lista_samochodow

def znajdz_dostepne_samochody(lista_samochodow):
    """Zwraca dostępne samochody."""
    return [samochod for samochod in lista_samochodow if samochod.dostepny]

def zarezerwuj_samochod(klient, samochod, data_startu, data_konca):
    """Rezerwuje samochód dla klienta."""
    if not samochod.dostepny:
        raise Exception("Samochód jest niedostępny")
    samochod.dostepny = False
    rezerwacja = Rezerwacja(len(rezerwacje) + 1, klient, samochod, data_startu, data_konca)
    rezerwacje.append(rezerwacja)
    return rezerwacja

def anuluj_rezerwacje(id_rezerwacji):
    """Anuluje rezerwację samochodu."""
    rezerwacja = next((r for r in rezerwacje if r.id_rezerwacji == id_rezerwacji), None)
    if rezerwacja:
        rezerwacja.samochod.dostepny = True
        rezerwacje.remove(rezerwacja)
        return True
    else:
        return False

def oblicz_koszt_wypozyczenia(cena_za_dzien, liczba_dni):
    """Oblicza koszt wypożyczenia."""
    if liczba_dni <= 0:
        raise ValueError("Liczba dni musi być większa niż 0")
    return cena_za_dzien * liczba_dni

# ------------------------------
# Dane przykładowe
# ------------------------------

samochody = []
klienci = []
rezerwacje = []
