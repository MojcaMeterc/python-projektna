import requests
import re
import random
import matplotlib.pyplot as plt
import matplotlib.patches as pathces


url = 'http://ufcstats.com/statistics/fighters?char=a&page=all'
html = requests.get(url).text

# Poišči vse vrstice v tabeli
vrstice = re.findall(r'<tr class="b-statistics__table-row">(.*?)</tr>', html, re.DOTALL)

borci = []

# Izbira podatkov iz vsake vrstice
for vrstica in vrstice:
    stolpci = re.findall(r'<td.*?>(.*?)</td>', vrstica, re.DOTALL)

    smooth = []

    # Obdelava vsake celice v vrstici
    for stolpec in stolpci:
        # Poišči vsebino v <a> oznakah (če obstaja)
        link = re.search(r'<a .*?>(.*?)</a>', stolpec, re.DOTALL)

        if link:
            # Če vsebina v <a> oznaki ni prazna, jo dodaj
            if not link.group(1).strip():
                smooth.append('/')  # Če ni besedila, nastavi na None
            else:
                smooth.append(link.group(1).strip())  # Dodaj besedilo iz <a>
        else:
            smooth.append(stolpec.strip())  # Če ni <a> oznake, dodaj običajno besedilo

    if len(smooth) >= 10:
        borec = {
            'Ime': smooth[0],
            'Priimek': smooth[1],
            'Vzdevek': smooth[2] if smooth[2] else None,  # Če ni nickname, nastavi na None
            'Višina': smooth[3],
            'Teža': smooth[4],
            'Doseg roke': smooth[5] if smooth[5] != '--' else None,  # Če ni dosega, nastavi na None
            'Drža': smooth[6] if smooth[6] != '--' else None,  # Če ni drže, nastavi na None
            'Zmage': int(smooth[7]),
            'Zgube': int(smooth[8]),
            'Izenačenja': int(smooth[9])
        }
        borci.append(borec)


def najdi_borca(ime):
    '''Funckijca vrne podatke borca'''
    '''uporabnik mora vnesti ime z malimi tiskanimi črkami'''
    ime = ime.lower()
    for borec in borci:
        celo_ime = f'{borec["Ime"]} {borec["Priimek"]}'.lower()
        if ime == borec['Ime'].lower() or ime == borec['Priimek'].lower() or ime == celo_ime:
            return borec
    return 'Borec ni bil najden'


def teznostna_skupina(teza):
    '''Vrne v katero težnostno skupino spada borec'''
    skupine = {
        (0, 115): 'Strawweight',
        (116, 125): 'Flyweight',
        (126, 135): 'Bantaweight',
        (136, 145): 'Featherweight',
        (146, 155): 'Lightweight',
        (156, 170): 'Welterweight',
        (171, 185): 'Middleweight',
        (186, 205): 'Light Heavyweight',
        (206, 265): 'Heavyweight'
    }
    for (min_teza, maks_teza), skupina in skupine.items():
        if min_teza <= teza <= maks_teza:
            return skupina
    return 'Super Heavyweight'


def risanje_kartice(borec1, borec2, teza):
    '''Risanje kartice borcev'''
    # Nastavitev figure
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_facecolor('lightgray')
    plt.axis('off')

    # Kartica za barvno ozadje
    kartica_x = 0.15
    kartica_sirina = 0.7
    kartica = pathces.FancyBboxPatch((kartica_x, 0.15), kartica_sirina, 0.7,
                                     boxstyle='round, pad=0.05',
                                     facecolor=('lightgrey', 0.3),
                                     alpha=0.2)
    ax.add_patch(kartica)

    # Naslov z imenom borca
    plt.text(0.5, 0.93, f"{borec1['Ime'].upper()} vs {borec2['Ime'].upper()}",
             ha='center', fontsize=30, fontweight='bold', color=('red', 0.8))

    # Podnaslov s ime kategorije teže
    plt.text(0.5, 0.85, f'{teza}', ha='center', fontsize=16, color='gray', style='italic')

    kategorije = ["Ime", "Priimek", "Višina", "Teža", "Doseg roke", "Drža"]
    n = len(kategorije)
    y_center = 0.5  # Središče kartice
    y_step = 0.1  # Razmik med vrsticami

    # Izračun začetne pozicije
    y_start = y_center +((n - 1) / 2) * y_step

    for i, kat in enumerate(kategorije):
        y = y_start - i * y_step
        plt.text(0.3, y, borec1[kat], ha='center', fontsize=14, color='black')
        plt.text(0.5, y, kat.upper(), ha='center', fontsize=14, color='black', fontweight='bold')
        plt.text(0.7, y, borec2[kat], ha='center', fontsize=14, color='black')
    plt.show()


def pridobi_tezo(borec):
    '''Preveri ali je za težo pravilni podatek'''
    teza = borec['Teža']
    if teza == '--':
        return None
    return teza.split()[0]


def ali_lahko_tekmujeta(borec1=None, borec2=None):
    '''Primerja teži dveh borcev ter preveri ali lahko tekmujeta.'''

    # Če noben od borcev ni podan izberemo naključno dva
    if borec1 is None and borec2 is None:
        borec1_slovar = random.choice(borci)
        borec2_slovar = random.choice(borci)
    else:

        borec1_slovar = najdi_borca(borec1)
        borec2_slovar = najdi_borca(borec2)

    # Preverimo ali borec obstaja
    if borec1_slovar == 'Borec ni bil najden' or borec2_slovar == 'Borec ni bil najden':
        raise ValueError('Eden od borcev ne obstaja')

    teza1 = pridobi_tezo(borec1_slovar)
    teza2 = pridobi_tezo(borec2_slovar)

    if teza1 is None or teza2 is None:
        return 'Borec nima znane teže.'

    borec1_skupina = teznostna_skupina(int(teza1))
    borec2_skupina = teznostna_skupina(int(teza2))

    if borec2_skupina != borec1_skupina:
        print(f'{borec1_slovar["Ime"]} in {borec2_slovar["Ime"]} nista v isti težnostni skupini. Ne morata tekmovati.')

    else:
        risanje_kartice(borec1_slovar, borec2_slovar, borec1_skupina)


ali_lahko_tekmujeta('Cyborg	Abreu', 'John Adajar')


# Dva borca, ki sta v isti težnostni skupini: Daichi Abe in  John Adajar
# Dva borca, ki nista v isti težnostni skupini: Zarrukh	Adashev in Mostapha	Al-Turk
# Če ne dobi nobenega imena funkcija naključno izbere dva borca