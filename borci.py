import matplotlib.pyplot as plt
import requests 
import re

def borci():
    url = "http://ufcstats.com/statistics/fighters?char=a&page=all"
    url = requests.get(url).text

    podatki_borca = re.findall(r'<a href="http://ufcstats.com/fighter-details/(.*?)" class="b-link b-link_style_black">(.*?)</a>', url, re.DOTALL)
    slovar = {}
    i = 0
    for podatek in podatki_borca:
        ime = podatek[i]
        priimek = [i+1]
        vzdevek = [i+2]
        



    return podatki_borca

print(borci())
