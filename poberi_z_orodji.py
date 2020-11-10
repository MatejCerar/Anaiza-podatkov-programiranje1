import orodja
import re
import requests
import json

stevilo_strani = 46
stevilo_viskijev_na_stran = 60
count = 0
slovarji_viskijev = []


def page_to_viskiji(page_content):

    vzorec = re.compile(r'<div class="information">(.*?)</a>', re.DOTALL)
    viskiji = [m.group(1).strip() for m in re.finditer(vzorec, page_content)]

    return viskiji

def get_dict_from_block(block):
    
    vzorec_ime= re.compile(r'<div class="name">(?P<ime>.*?)<', re.DOTALL)
    vzorec_cena = re.compile(r'<span class="price">(?P<cena>.*?)</span>', re.DOTALL)
    vzorec_kolicina = re.compile(r'<span class="meta">(?P<kolicina>.*?)\s/',re.DOTALL)
    vzorec_procent_alkohola = re.compile(r'<span class="meta">.*?/\s(?P<procent_alkohola>.*?)</span>', re.DOTALL)
    vzorec_cena_na_enoto = re.compile(r'<span class="price-meta">\((?P<cena_na_enoto>.*?)\)</span>', re.DOTALL)
    match_ime = re.search(vzorec_ime, block)
    match_cena = re.search(vzorec_cena, block)
    match_kolicina = re.search(vzorec_kolicina, block)
    match_procent_alkohola = re.search(vzorec_procent_alkohola, block)
    match_cena_na_enoto = re.search(vzorec_cena_na_enoto, block)

    slovar = {'ime': match_ime.group('ime') if match_ime is not None else None,
    'cena': match_cena.group('cena')if match_cena is not None else None,
    'kolicina': match_kolicina.group('kolicina')if match_kolicina is not None else None,
    'procent_alkohola': match_procent_alkohola.group('procent_alkohola')if match_procent_alkohola is not None else None, 
    'cena_na_enoto': match_cena_na_enoto.group('cena_na_enoto')if match_cena_na_enoto is not None else None}
    return slovar



for start in range(1, stevilo_strani + 1):
    url = f'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?pg={start}#productlist-filter'
    
    prvi_pobran = 1 + count * stevilo_viskijev_na_stran
    zadnji_pobran = (count + 1) * stevilo_viskijev_na_stran
    datoteka = f'Skotski_viskiji/{prvi_pobran}-{zadnji_pobran}.html'
    count +=1

    orodja.shrani_spletno_stran(url, datoteka)

    vsebina = orodja.vsebina_datoteke(datoteka) 
    viskiji = page_to_viskiji(vsebina)
    for viski in viskiji:
        slovarji_viskijev.append(get_dict_from_block(viski))

print(len(slovarji_viskijev))

orodja.zapisi_csv(slovarji_viskijev, slovarji_viskijev[0].keys(),'skotski_viskiji.csv')

with open ('skotski_viskiji.json', 'w') as f:
    json.dump (slovarji_viskijev, f, indent = 2, ensure_ascii = True)