import matplotlib.pyplot as plt
import requests 
import re

url = 'http://ufcstats.com/statistics/events/completed?page=all'
url = requests.get(url).text
url = url.split('  <ul class="b-statistics__paginate">')[0]
# re.DOTALL nam da tudi omogečen prestop v novo vrstico v regularnem izrazu
datumi = re.findall(r'<span class="b-statistics__date">(.*?)</span>', url, re.DOTALL)
datumi = [datum.strip() for datum in datumi]

# narisali bomo graf da predstavimo katero leto je bilo največ eventov in katero leto najmanj, oziroma kdaj je začelo postajati 
# 'popularno'
eventi_na_leto = {}
for datum in datumi:
    _, leto = datum.split(',')
    leta = leto.strip()
    eventi_na_leto[leta] = eventi_na_leto.get(leta, 0) + 1

leta_lepo, st_eventov = zip(*sorted(eventi_na_leto.items(), key=lambda x: x[0], reverse=True)[::-2])

plt.figure(figsize=(10,6))
plt.plot(leta_lepo, st_eventov, color='blue', marker='o', linestyle='-')
plt.xticks(rotation=45)
plt.xlabel('Leto')
plt.ylabel('Število dogodkov')
plt.title('UFC skozi leta')

plt.savefig(r'C:\Users\mojca\OneDrive\Namizje\PROG\python_projektna\graf_datumov.png')
plt.close()