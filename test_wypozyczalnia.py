import pytest
from wypozyczalnia import Samochod, Klient, dodaj_samochod, znajdz_dostepne_samochody, zarezerwuj_samochod, anuluj_rezerwacje, oblicz_koszt_wypozyczenia
from datetime import date, timedelta

# Przygotowanie danych
@pytest.fixture
def przykladowy_samochod():
    return Samochod(1, "Toyota", "Corolla", 100)

@pytest.fixture
def przykladowy_klient():
    return Klient(1, "Jan Kowalski", "jan@example.com")

# ------------------------------
# Testy do funkcji dodaj_samochod
# ------------------------------

def test_dodaj_samochod(przykladowy_samochod):
    samochody = []
    wynik = dodaj_samochod(samochody, przykladowy_samochod)
    assert przykladowy_samochod in wynik

def test_dodaj_samochod_zwieksza_dlugosc(przykladowy_samochod):
    samochody = []
    dodaj_samochod(samochody, przykladowy_samochod)
    assert len(samochody) == 1

def test_dodaj_wiele_samochodow():
    samochody = []
    s1 = Samochod(1, "Toyota", "Corolla", 100)
    s2 = Samochod(2, "BMW", "320i", 200)
    dodaj_samochod(samochody, s1)
    dodaj_samochod(samochody, s2)
    assert len(samochody) == 2

def test_dodaj_samochod_sprawdzenie_typu(przykladowy_samochod):
    samochody = []
    dodaj_samochod(samochody, przykladowy_samochod)
    assert isinstance(samochody[0], Samochod)

# ------------------------------
# Testy do funkcji znajdz_dostepne_samochody
# ------------------------------

def test_znajdz_dostepne_samochody(przykladowy_samochod):
    samochody = [przykladowy_samochod]
    dostepne = znajdz_dostepne_samochody(samochody)
    assert przykladowy_samochod in dostepne

def test_brak_dostepnych_samochodow():
    samochod = Samochod(1, "Ford", "Focus", 80, dostepny=False)
    samochody = [samochod]
    dostepne = znajdz_dostepne_samochody(samochody)
    assert len(dostepne) == 0

def test_wiele_dostepnych_samochodow():
    s1 = Samochod(1, "Toyota", "Corolla", 100, dostepny=True)
    s2 = Samochod(2, "BMW", "X3", 300, dostepny=True)
    samochody = [s1, s2]
    dostepne = znajdz_dostepne_samochody(samochody)
    assert len(dostepne) == 2

def test_czesciowo_dostepne_samochody():
    s1 = Samochod(1, "Audi", "A4", 150, dostepny=True)
    s2 = Samochod(2, "Audi", "A6", 200, dostepny=False)
    samochody = [s1, s2]
    dostepne = znajdz_dostepne_samochody(samochody)
    assert s1 in dostepne
    assert s2 not in dostepne

# ------------------------------
# Testy do funkcji zarezerwuj_samochod
# ------------------------------

def test_zarezerwuj_samochod_sukces(przykladowy_samochod, przykladowy_klient):
    start = date.today()
    koniec = start + timedelta(days=3)
    rezerwacja = zarezerwuj_samochod(przykladowy_klient, przykladowy_samochod, start, koniec)
    assert not rezerwacja.samochod.dostepny

def test_zarezerwuj_samochod_niedostepny(przykladowy_samochod, przykladowy_klient):
    przykladowy_samochod.dostepny = False
    start = date.today()
    koniec = start + timedelta(days=3)
    with pytest.raises(Exception):
        zarezerwuj_samochod(przykladowy_klient, przykladowy_samochod, start, koniec)

def test_rezerwacja_poprawna_cena(przykladowy_samochod, przykladowy_klient):
    start = date.today()
    koniec = start + timedelta(days=5)
    rezerwacja = zarezerwuj_samochod(przykladowy_klient, przykladowy_samochod, start, koniec)
    assert rezerwacja.calkowity_koszt == 5 * przykladowy_samochod.cena_za_dzien

def test_zwiekszenie_liczby_rezerwacji(przykladowy_samochod, przykladowy_klient):
    start = date.today()
    koniec = start + timedelta(days=2)
    liczba_rezerwacji = len(rezerwacje)
    zarezerwuj_samochod(przykladowy_klient, przykladowy_samochod, start, koniec)
    assert len(rezerwacje) == liczba_rezerwacji + 1

# ------------------------------
# Testy do funkcji anuluj_rezerwacje
# ------------------------------

def test_anuluj_istniejaca_rezerwacje(przykladowy_samochod, przykladowy_klient):
    start = date.today()
    koniec = start + timedelta(days=2)
    rezerwacja = zarezerwuj_samochod(przykladowy_klient, przykladowy_samochod, start, koniec)
    sukces = anuluj_rezerwacje(rezerwacja.id_rezerwacji)
    assert sukces == True

def test_anuluj_nieistniejaca_rezerwacje():
    sukces = anuluj_rezerwacje(999)
    assert sukces == False

def test_po_anulowaniu_samochod_dostepny(przykladowy_samochod, przykladowy_klient):
    start = date.today()
    koniec = start + timedelta(days=1)
    rezerwacja = zarezerwuj_samochod(przykladowy_klient, przykladowy_samochod, start, koniec)
    anuluj_rezerwacje(rezerwacja.id_rezerwacji)
    assert przykladowy_samochod.dostepny == True

def test_po_anulowaniu_brak_rezerwacji(przykladowy_samochod, przykladowy_klient):
    start = date.today()
    koniec = start + timedelta(days=1)
    rezerwacja = zarezerwuj_samochod(przykladowy_klient, przykladowy_samochod, start, koniec)
    anuluj_rezerwacje(rezerwacja.id_rezerwacji)
    assert rezerwacja not in rezerwacje

# ------------------------------
# Testy do funkcji oblicz_koszt_wypozyczenia
# ------------------------------

def test_oblicz_koszt_wypozyczenia_poprawny():
    assert oblicz_koszt_wypozyczenia(100, 5) == 500

def test_oblicz_koszt_wypozyczenia_zero_dni():
    with pytest.raises(ValueError):
        oblicz_koszt_wypozyczenia(100, 0)

def test_oblicz_koszt_wypozyczenia_ujemne_dni():
    with pytest.raises(ValueError):
        oblicz_koszt_wypozyczenia(100, -3)

def test_oblicz_koszt_wypozyczenia_duze_wartosci():
    assert oblicz_koszt_wypozyczenia(1000, 100) == 100000
