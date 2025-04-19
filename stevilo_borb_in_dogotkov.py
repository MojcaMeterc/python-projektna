import requests
import re
import matplotlib.pyplot as plt
import random


def pridobi_html(url):
    '''Pridobimo potrebno povezavo'''
    return requests.get(url).text


def pridobi_dogodke(html):
    '''Shranimo leto ter povezavo do posameznega dogodtka'''
    dogodtki = []

    bloks = re.findall(r'<i class="b-statistics__table-content">(.*?)</i>', html, re.DOTALL)

    for blok in bloks:
        url_match = re.search(r'<a href="(http.*?)"', blok)
        datum_match = re.search(r'<span class="b-statistics__date">\s*(.*?)\s</span>', blok, re.DOTALL)

        if url_match and datum_match:
            url = url_match.group(1).strip()
            datum = datum_match.group(1).strip()

            try:
                datum, leto = datum.split(',')

                dogodtki.append({'url': url, 'leto': leto, 'datum': datum})
            except ValueError:
                continue

    return dogodtki

def dogodtki_glede_na_mesec(izbrana_leta):
    base_url = 'http://ufcstats.com/statistics/events/completed?page=all'
    html = pridobi_html(base_url)
    podatki = pridobi_dogodke(html)

    meseci = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    
    izbrana_leta = {str(leto) for leto in izbrana_leta}

    # Zberi mesece po letih
    dogodki_po_letih = {}
    for dogodek in podatki:
        datum = dogodek['datum'].strip()
        leto = dogodek['leto'].strip()
        mesec = datum.split()[0]

        if leto in izbrana_leta:
            dogodki_po_letih.setdefault(leto, []).append(mesec)

    # Preštej dogodke po mesecih
    rezultat = {}
    for leto in izbrana_leta:
        rezultat[leto] = {mesec: 0 for mesec in meseci}
        if leto in dogodki_po_letih:
            for mesec in dogodki_po_letih[leto]:
                if mesec in meseci:
                    rezultat[leto][mesec] += 1

    return rezultat

def prestej_borbe(url):
    '''prešteje borbe'''
    html = requests.get(url).text
    return(len(re.findall(r'<tr class="b-fight-details__table-row[^>]*js-fight-details-click', html, re.DOTALL)))

def stevilo_dogodkotv():
    base_url = 'http://ufcstats.com/statistics/events/completed?page=all'
    html = pridobi_html(base_url)
    podatki = pridobi_dogodke(html)
    stevilo_na_leto = {}

    for dogodek in podatki:
        url = dogodek['url']
        leto = dogodek['leto']

        if leto not in stevilo_na_leto:
            stevilo_na_leto[leto] = 0
        stevilo_na_leto[leto] += 1
    return stevilo_na_leto

def povprecje(slovar):
    poveprecje = {}
    for leto, stevilo_borb in slovar.items():
        poveprecje[leto.strip()] = int(sum(stevilo_borb)/len(stevilo_borb))
    return poveprecje

def poljubna_leta_povprecje(leta):
    base_url = 'http://ufcstats.com/statistics/events/completed?page=all'
    html = pridobi_html(base_url)
    podatki = pridobi_dogodke(html)
    stevilo_borb= {}

    leta = set(str(leto).strip() for leto in leta)
    filtrirano = [dogodek for dogodek in podatki if dogodek['leto'].strip() in leta]
    for dogodek in filtrirano:
        url = dogodek['url']
        leto = dogodek['leto']

        borbe = prestej_borbe(url)

        stevilo_borb.setdefault(leto, []).append(borbe)

    return povprecje(stevilo_borb)


def povprecno_stevilo_borb_dolocenih():
    base_url = 'http://ufcstats.com/statistics/events/completed?page=all'
    html = pridobi_html(base_url)
    podatki = pridobi_dogodke(html)
    vsako_3_leto = [dogodek for dogodek in podatki if int(dogodek['leto']) % 3 == 0]
    stevilo_borb = {}

    for dogodek in vsako_3_leto:
        url = dogodek['url']
        leto = dogodek['leto']

        borbe = prestej_borbe(url)
        stevilo_borb.setdefault(leto, []).append(borbe)

    return povprecje(stevilo_borb)

def nakljucna_barva():
    return '#{:06x}'.format(random.randint(0, 0xFFFFFF))

def narisi_graf():
    print('Izberiti kateri graf želite videti. Izbirate lahko med:\n ' \
    '-Število dogotkov na leto (1), \n'\
    '-Povprečno število borb na leto (pogleda vsak dogodek) (2),\n' \
    '-Število dogotkov na mesec v letu (3)')

    graf = input('Vnesi število (napisana je na koncu vsakega grafa): ')

    if graf == '2':
        print('Za ta graf lahko samo izberete poljubna leta za izpis. Če želite izbrati leta vnesite 1 \n' \
        'drugače pa 2 in bo program narisal graf z vsakim tretjim letom. Ko ne želiš več vnesti leto napiši "konec"')
        odgovor = input('Vnesi željeno število grafa: ')

        if odgovor == '1':
            letnice = []
            print('Priporočam maksimalno 6 let')
            while True:
                vnos = input('Vnesi leto: ')
                if vnos.lower() == 'konec':
                    break
                else:
                    letnice.append(str(vnos))
            if len(letnice) > 10:
                print('To bo malo trajalo. Upam, da se ti ne mudi :)')

            podatki = poljubna_leta_povprecje(letnice)
            leta = [leta.strip() for leta in podatki.keys()]
            leta = leta[::-1]
            borbe = [borba for borba in podatki.values()]
            borbe = borbe[::-1]
            plt.bar(leta, borbe, color='lightblue')
            plt.title('Povprečno število borb glede dogodek in leto')
            plt.xlabel('Leta')
            plt.ylabel('Povprečno število borb')
            plt.xticks(leta, rotation=45)
            plt.show()

        else:
            povprecje_borb =  povprecno_stevilo_borb_dolocenih()
            leta = [leta.strip() for leta in povprecje_borb.keys()]
            leta = leta[::-1]
            borbe = [borba for borba in povprecje_borb.values()]
            borbe = borbe[::-1]
            plt.bar(leta, borbe, color='lightblue')
            plt.title('Povprečno število borb glede dogodek in leto')
            plt.xlabel('Leta')
            plt.ylabel('Povprečno število borb')
            plt.xticks(leta, rotation=45)
            plt.show()

    elif graf == '1':
        na_leto = stevilo_dogodkotv()
        leta = [leta.strip() for leta in na_leto.keys()]
        leta = leta[::-1]
        borbe = [borba for borba in na_leto.values()]
        borbe = borbe[::-1]

        plt.figure(figsize=(10,7))
        stoplci = plt.bar(leta, borbe, color='pink')
        plt.title('Število dogodtkov na leto')
        plt.xlabel('Leta')
        plt.ylabel('Število borb na leto')
        plt.xticks(leta, rotation=45)
        for i, stolpec in enumerate(stoplci):
            plt.annotate(str(borbe[i]),
                        xy = (stolpec.get_x() + stolpec.get_width() / 2,\
                        stolpec.get_height()),
                        xytext=(0,3),
                        textcoords='offset points',
                        ha = 'center',
                        va= 'bottom',
                        fontsize= 8,
                        color= 'pink')
        plt.tight_layout()
        plt.show()

    else:
        meseci = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
        leta = []
        while True:
            vnos = input('Vnesi leto: ')
            if vnos.lower() == 'konec':
                break
            else:
                leta.append(str(vnos))
        podatki = dogodtki_glede_na_mesec(leta)

        plt.figure(figsize=(15, 7))
        for leto, mesec_podatki in podatki.items():
            vrednosti = [mesec_podatki[mesec] for mesec in meseci]
            barva = nakljucna_barva()
            plt.plot(meseci, vrednosti, marker='o', label=leto, color=barva)

        plt.title('Mesečni podatki glede na leto')
        plt.xlabel('Mesec')
        plt.ylabel('Število dogodtkov')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.show()
narisi_graf()