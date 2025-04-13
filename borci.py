import matplotlib.pyplot as plt
import requests 
import re

class Borec:
    def __init__(self, ime, priimek, vzdevek = None, visina = None,\
                 teza = None, doseg = None):
        self._ime = ime
        self._priimek = priimek
        self._vzdevek = vzdevek
        self._visina = visina
        self._teza = teza
        self._doseg = doseg

    def __str__(self):
        return f'{self._ime}, {self._priimek}, ({self._ime}): teža: {self._teza}, višina: {self._visina}, doseg: {self._doseg}'

def borci_osebni_podatki():
    url = "http://ufcstats.com/statistics/fighters?char=a&page=all"
    url = requests.get(url).text

    podatki_borcev = re.findall(r'<a href="http://ufcstats.com/fighter-details/(.*?)" class="b-link b-link_style_black">(.*?)</a>', url, re.DOTALL)

    vrednosti = [v for _, v in podatki_borcev]
    osebe = []
    for i in range(0, len(vrednosti), 3):
        oseba = {'ime': vrednosti[i],
                 'priimek': vrednosti[i+1],
                 'vzdevek': vrednosti[i+2]}
        
        osebe.append(oseba)
    return osebe

def borci_drugi_podatki():
    url = "http://ufcstats.com/statistics/fighters?char=a&page=all"
    url = requests.get(url).text
    podatki = re.findall(r'<td class="b-statistics__table-col"\s*(.*?)\s*</td>', url, re.DOTALL)
    print(podatki)


def zdruzi():
    osebe = borci_osebni_podatki()
    visina, teza, doseg = borci_drugi_podatki()
    

    borci = []
    for i in range(len(osebe)):
        ime = osebe[i]['ime']
        priimek = osebe[i]['priimek']
        vzdevek = osebe[i].get('vzdevek', None)

        visina_borca = visina[i] if i < len(visina) else None
        teza_borca = teza[i] if i < len(teza) else None
        doseg_borca = doseg[i] if i < len(doseg) else None

        borec = Borec(ime, priimek, vzdevek, visina_borca, teza_borca, doseg_borca)
        borci.append(borec)
        
    return borci

borci_drugi_podatki()

    




