import requests
import re

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
            'First name': smooth[0],
            'Last name': smooth[1],
            'Nickname': smooth[2] if smooth[2] else None,  # Če ni nickname, nastavi na None
            'Height': smooth[3],
            'Weight': smooth[4],
            'Doseg roke': smooth[5] if smooth[5] != '--' else None,  # Če ni dosega, nastavi na None
            'Drža': smooth[6] if smooth[6] != '--' else None,  # Če ni drže, nastavi na None
            'Wins': int(smooth[7]),
            'Losses': int(smooth[8]),
            'Draws': int(smooth[9])
        }
        borci.append(borec)

# Funkcija za iskanje borca po imenu
def najdi_borca(name):
    '''uporabnik mora vnesti ime z malimi tiskanimi črkami'''
    for borec in borci:
        full_name = f'{borec["First name"]} {borec["Last name"]}'.lower()
        if name == borec['First name'].lower() or name == borec['Last name'].lower() or name == full_name:
            return borec
    return 'Fighter not found.'

# Preizkusi iskanje borca
ime = 'tom aaron'
print(najdi_borca(ime))
