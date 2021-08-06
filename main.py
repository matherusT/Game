import pygame
import random
import math
from pygame import  mixer
import os, sys


def resource_path(relative_path):
    try:
        base_path = sys.__MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)

# okno
pygame.init()
okno = pygame.display.set_mode((800, 600))

# nazwa
pygame.display.set_caption("Gra")

# logo
url_logo = resource_path('ikony/helmet.png')
logo = pygame.image.load(url_logo)
pygame.display.set_icon(logo)

# wynik
punkty = 0
url_czcionka = resource_path('Czcionka/VertigoFLF.ttf')
czcionka = pygame.font.Font(url_czcionka, 40)
punkty_wyswietlanieX = 500
punkty_wyswietlanieY = 550

# koniec gry czcoionka
url_czcionka2 = resource_path('Czcionka/VertigoFLF.ttf')
czcionka2 = pygame.font.Font(url_czcionka2, 85)
koniec_gryX = 300
koniec_gryY = 200

# gracz
url_gracz = resource_path('ikony/knight.png')
gracz = pygame.image.load(url_gracz)
graczX = 368
graczY = 500
przesuniecie_X = 0
przesuniecie_Y = 0

# przeciwnik
przeciwnik = []
przeciwnikX = []
przeciwnikY = []
przesuniecie_Y_przeciwnik = []
przesuniecie_X_przeciwnik = []

# bron
url_bron = resource_path('ikony/arrow.png')
bron = pygame.image.load(url_bron)
bronX = 368
bronY = 500
przesuniecie_Y_bron = 0
przesuniecie_X_bron = 0
bron_czy_gotowa = "Gotowa"

#dzwiek tlo
url_tlo = resource_path('Dzwieki/tlo.mp3')
mixer.music.load(url_tlo)
mixer.music.play(-1)
mixer.music.set_volume(0.1)


def koniec_gry(x, y):
    tekst = czcionka2.render('KONIEC GRY', True, (0, 0, 0))
    tekst2 = czcionka.render('Twój wynik: ' + str(punkty), True, (0, 0, 0))
    tekst3 = czcionka.render('Nacisni r, jesli chcesz zagrac jeszcze raz', True, (0, 0, 0))
    okno.blit(tekst, (x, y))
    okno.blit(tekst2, (x + 50, y + 85))
    okno.blit(tekst3, (x - 80, y + 120))



def gracz_wyswietl(x, y):
    okno.blit(gracz, (x, y))


def przeciwnik_wyswietl(x, y, i):
    okno.blit(przeciwnik[i], (x, y))


def strzal(x, y):
    global bron_czy_gotowa
    okno.blit(bron, (x + 32, y))
    bron_czy_gotowa = "Rzucona"


def kolizja(wrogX, wrogY, bronX, bronY):
    d = math.sqrt(((wrogX - bronX) ** 2) + ((wrogY - bronY) ** 2))
    if d < 25:
        return True


def punkty_wyswietlanie(x, y):
    tekst = czcionka.render('Wynik: ' + str(punkty), True, (0, 0, 0))
    okno.blit(tekst, (x, y))


def nowa_gra():
    global punkty, przegrana, n, przeciwnikX, przeciwnikY, przesuniecie_X_przeciwnik, graczX, graczY
    punkty = 0
    przegrana = False
    graczX = 368
    graczY = 500
    przeciwnik.clear()
    przeciwnikX.clear()
    przeciwnikY.clear()
    przesuniecie_X_przeciwnik.clear()
    url_dzwiek_nowa_gra = resource_path('Dzwieki/nowa-gra.wav')
    dzwiek_nowa_gra = mixer.Sound(url_dzwiek_nowa_gra)
    dzwiek_nowa_gra.play()
    for i in range(2):
        nowy_przeciwnik()

def nowy_przeciwnik():
    global przeciwnik, przeciwnikX, przeciwnikY, przesuniecie_X_przeciwnik, url_przeciwnik
    url_przeciwnik = resource_path('ikony/ninja.png')
    przeciwnik.append(pygame.image.load(url_przeciwnik))
    przeciwnikX.append(random.randint(0, 730))
    przeciwnikY.append(random.randint(0, 150))
    przesuniecie_X_przeciwnik.append((random.randint(1, 10) / 10))


for i in range(2):
    nowy_przeciwnik()

przegrana = False
gra = True
while gra:
    okno.fill((36, 55, 27))

    punkty_wyswietlanie(punkty_wyswietlanieX, punkty_wyswietlanieY)
    gracz_wyswietl(graczX, graczY)
    graczX += przesuniecie_X
    graczY += przesuniecie_Y

    bronY += przesuniecie_Y_bron

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bron_czy_gotowa == "Gotowa":
                    strzal(bronX, bronY)
                    url_dzwiek_strzal = resource_path('Dzwieki/strzal.wav')
                    dzwiek_strzal = mixer.Sound(url_dzwiek_strzal)
                    dzwiek_strzal.play()
                    bronX = graczX
                    bronY = graczY

            if przegrana:
                if event.key == pygame.K_r:
                    nowa_gra()

    # poruszanie sie (gracz)
    nacisniete_klaw = pygame.key.get_pressed()
    przesuniecie_Y = 0
    przesuniecie_X = 0

    if przegrana == False:
        if nacisniete_klaw[pygame.K_LEFT]:
            przesuniecie_X = -1

        elif nacisniete_klaw[pygame.K_RIGHT]:
            przesuniecie_X = 1

        if nacisniete_klaw[pygame.K_DOWN]:
            przesuniecie_Y = 1

        elif nacisniete_klaw[pygame.K_UP]:
            przesuniecie_Y = -1

        if bron_czy_gotowa == "Rzucona":
            strzal(bronX, bronY)
            przesuniecie_Y_bron = -3

        if bronY < -50:
            bron_czy_gotowa = "Gotowa"

        # poruszanie sie (przeciwnik)
        for i in range(len(przeciwnik)):
            if przeciwnikX[i] <= 0:
                przesuniecie_X_przeciwnik[i] *= -1
                przeciwnikY[i] += 32
            elif przeciwnikX[i] >= 736:
                przesuniecie_X_przeciwnik[i] *= -1
                przeciwnikY[i] += 32

            # trafienie przeciwnika
            if kolizja(przeciwnikX[i], przeciwnikY[i], bronX, bronY):
                nowy_przeciwnik()
                bron_czy_gotowa = "Gotowa"
                url_dzwiek_trafienie = resource_path('Dzwieki/trafienie.wav')
                dzwiek_trafienie = mixer.Sound(url_dzwiek_trafienie)
                dzwiek_trafienie.play()
                dzwiek_trafienie.set_volume(0.1)
                url_dzwiek_punkt = resource_path('Dzwieki/punkt.wav')
                dzwiek_punkt = mixer.Sound(url_dzwiek_punkt)
                dzwiek_punkt.play()
                przeciwnikX[i] = random.randint(0, 730)
                przeciwnikY[i] = 0
                punkty += 1
                bronY = -100

            przeciwnik_wyswietl(przeciwnikX[i], przeciwnikY[i], i)
            przeciwnikX[i] += przesuniecie_X_przeciwnik[i]

            if przeciwnikY[i] >= 300:
                for i in range(len(przeciwnik)):
                    przeciwnikY[i] = -100
                    przesuniecie_X_przeciwnik[i] = 0
                    przegrana = True

            if kolizja(przeciwnikX[i], przeciwnikY[i], graczX, graczY):
                for i in range(len(przeciwnik)):
                    przeciwnikY[i] = -100
                    przesuniecie_X_przeciwnik[i] = 0
                    przegrana = True

    if przegrana:
        koniec_gry(koniec_gryX, koniec_gryY)

    # ograniczniki w poruszaniu sie (gracz)
    if graczX > 752:
        graczX = 752

    elif graczX < -16:
        graczX = -16

    if graczY > 536:
        graczY = 536

    elif graczY < 0:
        graczY = 0

    pygame.display.update()
