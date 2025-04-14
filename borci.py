import requests
import re

url = 'http://ufcstats.com/statistics/fighters?char=a&page=all'
html = requests.get(url).text

rows = re.findall(r'<tr class="b-statistics__table-row">(.*?)</tr>', html, re.DOTALL)

fighters = []

for row in rows:
    columns = re.findall(r'<td.*?>(.*?)</td>', row, re.DOTALL)

    smooth = []
     
    for column in columns:
        link = re.search(r'>([^<]+)<', column)

        if link:
            # ko iščeš tekst med > <, nas zanima samo vsebima in ne ostale oznake <a> zato uporabimo group(1)
            smooth.append(link.group(1).strip())
        else:
            smooth.append(column.strip())
    if len(smooth) >= 10:
        # tuki dopolni kaj je w, l, d z besedo ker jz nevem kaj je
        # pa ce kj ni pomembn odstran recmo reach al pa stance k tud nevem kaj je
        fighter = { 'First name': smooth[0],
                   'Last name': smooth[1],
                   'Nickname': smooth[2],
                   'Height': smooth[3],
                   'Weight': smooth[4],
                   'Doseg roke': smooth[5] if smooth[5] != '--' else None,
                   'Drža': smooth[6] if smooth[6] != '--' else None,
                   'Zmage': int(smooth[7]),
                   'Poraz': int(smooth[8]),
                   'Izenačenje': int(smooth[9])}
        fighters.append(fighter)

def find_fighter(name):
    '''uporabnik mora vnesti imez malimi tiskanimi črkami'''
    for fighter in fighters:
        full_name = f'{fighter["First name"]} {fighter["Last name"]}'.lower()
        if name == fighter['First name'].lower() or name == fighter['Last name'].lower() or name == full_name:
            return fighter
    return 'Fighter not found.'

ime = 'mansur abdul-malik'
print(find_fighter(ime))

# primeri imen, če uporabnik ne pozna nobenega: nariman, abe, aguilar, omari, rostem akman...