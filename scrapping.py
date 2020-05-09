import json
import pickle
import bs4
import requests
import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_soup(url):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    res = session.get(url)
    soup = bs4.BeautifulSoup(res.text)
    return soup

def source_code(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    code = (str(soup.contents).replace("['", "").replace("']", "").replace(r'\'', ""))
    return json.loads(code)

def get_ids():
    lista = []
    enderecos = ['data(1).json','data(2).json','data(3).json','data(4).json','data.json']
    x = [json.loads(open(i,"r").read()) for i in enderecos]
    for z in x:
        for i in z:
            id = i['account_id']
            if id not  in lista:
                lista.append(id)
    return lista

def get(id,dict):
    url1 = 'https://api.opendota.com/api/players/'

    dict.update({id:{}})
    url = url1+id
    code = source_code(url)
    if 'solo_competitive_rank' in code.keys() and code['solo_competitive_rank'] !=None:
        rank = code['solo_competitive_rank']
    else: rank = 0
    dict[id].update({"rank":rank})

    url = url1+ id + '/wl?'
    code = source_code(url)

    dict[id].update({"winrate": [code['win'], code['lose']]})

    url = url1 + id + '/heroes?'
    code = source_code(url)
    dict[id].update({"heroes": {}})
    for i in code:
            dict[id]["heroes"].update({i['hero_id']:[i['win'],i['games']]})

    url = url1 + id + "/matches?significant=0"
    code = source_code(url)
    dict[id].update({"recent_winrate": {}})
    n = 0
    win = 0
    lose = 0
    for i in code:
        if n == 10:
            break
        if (i['player_slot'] < 5 and i['radiant_win'] == True) or (i['player_slot'] > 5 and i['radiant_win'] == False):
            win = win + 1

        else: lose = lose + 1

        n = n + 1

        dict[id].update({"recent_winrate": [win, lose]})


    return dict

def ler(endereco):
    try:
        arq = open(endereco, 'rb')
    except:
        return {}
    return pickle.load(arq)

def salvar(endereco, lista):
    arq = open(endereco, 'wb')
    pickle.dump(lista, arq)
