import requests
import re
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def pridobi_html(url):
    return requests.get(url).text

def pridobi_dogodke(html):
    events = []

    bloks = re.findall(r'<i class="b-statistics__table-content">(.*?)</i>', html, re.DOTALL)
    
    for blok in bloks:
        url_match = re.search(r'<a href="(http.*?)"', blok)
        datum_match = re.search(r'<span class="b-statistics_date">\s*(.*?)\s</span>', blok)
    
        if url_match and datum_match:
            url = url_match.strip()
            datum = datum_match.strip()
 
            try:
                year = datetime.strptime(datum.strip(), "%B %d, %Y")
                events.append({'url': url.strip(), 'leto': year})
            except ValueError:
                continue
    print(events) 
    return events


def število_borb(url):
    html = pridobi_html(url)
    fights = re.findall(r'<a class="b-flag b-flag_style_green"', html, re.DOTALL)
    return len(fights)

def povprecje_na_leto():
    base_url = 'http://ufcstats.com/statistics/events/completed?page=all'
    html = pridobi_html(base_url)
    events = pridobi_dogodke(html)

    data_by_year = {}

    for event in events:
        year = event['leto']
        fight_num = število_borb(event['url'])

        if year not in data_by_year:
            data_by_year[year] = []
        
        data_by_year[year].append(fight_num)

    years = []
    averages = []
    # povprečno št borb na dogodek na leto
    for year in sorted(data_by_year.keys()):
        fights = data_by_year[year]
        average = sum(fights) / len(fights)
        years.append(year)
        averages.append(average)
    
    return years, averages

years, averages = povprecje_na_leto()

plt.figure(figsize=(10,5))
plt.bar(years, averages, color='skyblue')
plt.title('Povprečno število na dogodek po letih')
plt.xlabel('Leta')
plt.ylabel('Št. borb na dogodek')
plt.xticks(years, rotation=45)
plt.show()

