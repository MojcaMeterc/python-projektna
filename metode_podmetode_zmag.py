import requests
import re
import matplotlib.pyplot as plt

# Glavna struktura
metode_zmag = {'U-DEC': {},
               'SUB': {},
               'KO/TKO': {}}

url_zacetna = 'http://ufcstats.com/statistics/events/completed?page=all'
html = requests.get(url_zacetna).text
eventi = re.findall(r'<a href="(http://ufcstats.com/event-details/.*?)"', html, re.DOTALL)

# zbiranje metod in podmetod
# spustimo prvi element ker je to povezava do eventa, ki se še ni zgodil
for event in eventi[1:]:
    event_html = requests.get(event).text
    pari_metod = re.findall(r'<p class="b-fight-details__table-text">\s*([A-Z\-\/]+)\s*</p>\s*<p class="b-fight-details__table-text">\s*([^<]+?)\s*</p>', event_html, re.DOTALL)

    for metoda, način in pari_metod:
        if metoda == 'U-DEC':
            metode_zmag['U-DEC'] = metode_zmag.get('U-DEC', 0) + 1
        if metoda in metode_zmag and način != ' ':
            metode_zmag[metoda][način] = metode_zmag[metoda].get(način, 0) + 1

# priprava za tortni graf in 'risanje' grafa
imena = list(metode_zmag.keys())
velikosti = [sum(podmetoda.values()) for podmetoda in metode_zmag.values()]
barve = ['lightblue', 'lightpink', 'lightgreen']

oznake = []
for i in range(len(imena)):
    odstotek = velikosti[i] / sum(velikosti) * 100
    oznake.append(f'{imena[i]}: {velikosti[i]} ({odstotek:.1f}%)')

plt.figure(figsize=(10,8))
plt.pie(velikosti, labels=oznake, startangle=140, colors=barve)
plt.title('Načini zmage pri UFC-ju')
plt.axis('equal')
plt.savefig(r'C:\Users\mojca\OneDrive\Namizje\PROG\python_projektna\metode_zmag.png')
plt.close()

# stolpični grafi za vsako kategorijo
def narisi_graf(metoda_zmage, barva, naslov, shranitev_dat):
    plt.figure(figsize=(30,10))
    nacini_zmage = list(metoda_zmage.keys())
    stevilo = list(metoda_zmage.values())

    plt.bar(nacini_zmage, stevilo, color=barva)
    plt.xlabel('Načini metode')
    plt.ylabel('Število zmag na tak način')
    plt.title(naslov)
    plt.xticks(rotation=30)
    plt.savefig(shranitev_dat)
    plt.close()

# klici za vsako metodo posebaj
# metoda U-DEC nima različnih načinov zmage, ker pri tem sodniki odločajo kdo zmaga in se nanaša na celotno borbo
narisi_graf(metode_zmag['SUB'], 'palegreen', 'Načini zmage SUB', r'C:\Users\mojca\OneDrive\Namizje\PROG\python_projektna\sub.png')
narisi_graf(metode_zmag['KO/TKO'], 'lightpink', 'Načini zmage KO/TKO', r'C:\Users\mojca\OneDrive\Namizje\PROG\python_projektna\ko_tko.png')
