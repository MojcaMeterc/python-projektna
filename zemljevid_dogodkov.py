import requests
import re
import matplotlib.pyplot as plt
import geopandas
import geodatasets


url = 'http://ufcstats.com/statistics/events/completed?page=all'
html = requests.get(url).text
html = html.split('<ul class="b-statistics__paginate">')[0]

# Lokacije dogodkov
drzave = re.findall(r'<td class="b-statistics__table-col b-statistics__table-col_style_big-top-padding">(.*?)</td>', html, re.DOTALL)
drzave = [drzava.split(',') for drzava in drzave]
urejeni_pod = [drzava if len(drzava) == 3 else [drzava[0], 'Neznano', drzava[1]] for drzava in drzave]
mesta, state, drzave = zip(*urejeni_pod)

# Preštejemo dogodke na enaki lokaciji
st_eventov = {}
for par in zip(mesta, drzave):
    if par in st_eventov:
        st_eventov[par] += 1
    else:
        st_eventov[par] = 1


# Iskanje koordinat na internetu
def pridobi_koord(mesto, drzava):
    try:
        url = f'https://nominatim.openstreetmap.org/search?q={mesto},{drzava}&format=json&limit=1'
        headers = {'User-Agent': 'ufc_map_light'}
        json = requests.get(url, headers=headers).json()
        lat = float(json[0]['lat'])
        lon = float(json[0]['lon'])
        return lon, lat
    except:
        return None


lokacije = []
for (mesto, drzava), stevilo in st_eventov.items():
    koordinata = pridobi_koord(mesto, drzava)
    if koordinata:
        lon, lat = koordinata
        lokacije.append((lon, lat, stevilo))

# Narišemo zemljevid z knjižnico geopandas
pot = geodatasets.get_path('naturalearth.land')
df = geopandas.read_file(pot)
fig, ax = plt.subplots(figsize=(14, 8))
df.plot(ax=ax, alpha=0.5, edgecolor='k')  # Alpha določa prosojnost
# ax = ax: riše na zemljevid ki smo ga ustvarili

# Dodamo še dogodke na zemljevid
for lon, lat, stevilo in lokacije:
    ax.scatter(lon, lat, s=stevilo*15, color='pink', alpha=0.6, edgecolors='black')

plt.title('UFC dogodki po svetu (velikost krogca = število eventov)')
plt.axis('off')
plt.tight_layout()
plt.savefig('zemljevid_dogodkov.png')