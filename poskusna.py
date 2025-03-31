import matplotlib.pyplot as plt
import requests 
import re

url_1 = 'http://ufcstats.com/statistics/events/completed?page=all'
url_1 = requests.get(url_1).text
url_1 = url_1.split('  <ul class="b-statistics__paginate">')[0]
# re.DOTALL nam da tudi omogečen prestop v novo vrstico v regularnem izrazu
datumi = re.findall(r'<span class="b-statistics__date">(.*?)</span>', url_1, re.DOTALL)
datumi = [datum.strip() for datum in datumi]
print(datumi)

#isto k za datume se za mesta/države

