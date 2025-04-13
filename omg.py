

import requests
from bs4 import BeautifulSoup

def borci_dodatni_podatki():
    url = "http://ufcstats.com/statistics/fighters?char=a&page=all"
    html = requests.get(url).text
    # Uporabimo "lxml" parser; če nimaš nameščenega, ga lahko namestiš s pip
    soup = BeautifulSoup(html, 'lxml')
    
    # Poiščemo vse vrstice v tabeli, kjer so podatki o borcih
    rows = soup.find_all('tr', class_='b-statistics__table-row')
    
    borci = []
    for row in rows:
        # V vsaki vrstici so vsi podatki v <td> elementih z danim razredom
        cells = row.find_all('td', class_='b-statistics__table-col')
        # Prepričaj se, da je vrstica vsaj dolgo dovolj (v nasprotnem primeru se preskoči)
        if len(cells) >= 6:
            # Glede na strukturo:
            # Indeks 0, 1, 2 so verjetno povezani z osebnimi podatki (ime, priimek, vzdevek)
            # Indeks 3: Višina
            # Indeks 4: Teža
            # Indeks 5: Doseg
            # Indeks 6: Stance  
            # Če ima vrstica več podatkov, se prilagodi glede na dejansko strukturo strani.
            # Če imaš npr. 8 podatkov in ti te štiri pridejo na indeksih 3,4,5,6, potem:
            height = cells[3].get_text(strip=True)
            weight = cells[4].get_text(strip=True)
            reach  = cells[5].get_text(strip=True)
            stance = cells[6].get_text(strip=True)
            
            # Lahko obdržiš "--" ali preslikaš v None, če podatka ni.
            fighter_data = {
                "height": height,
                "weight": weight,
                "reach": reach,
                "stance": stance
            }
            borci.append(fighter_data)
    
    return borci

# Primer klica funkcije:
dodatni_podatki = borci_dodatni_podatki()
for fighter in dodatni_podatki:
    print(fighter)

