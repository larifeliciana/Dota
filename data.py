import json
import os
import pickle

def ler(endereco):
    arq = open(endereco, 'rb')
    return pickle.load(arq)

def salvar(endereco, lista):
    arq = open(endereco, 'wb')
    pickle.dump(lista, arq)

def carregar(pasta):
    caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
    lista = []
    for i in caminhos:
        data = json.load(open(i, 'r'))
        lista.append(data)
    return lista

def script(caracteristicas_partida, caracteristicas_jogador):
    dota = carregar('Data')
    vetor = {}
    for data in dota:
        print('*')
        for i in data:
            if i["match_id"] not in vetor.keys():
                vetor.update({(i["match_id"]):[i[j] for j in caracteristicas_partida]})
            vetor[i["match_id"]] = vetor[i["match_id"]] + [i[j] for j in caracteristicas_jogador]
    vetor =  list(vetor.values())
    return vetor

"""def script(dict, caracteristicas_partida, caracteristicas_jogador):

    vetor = {}
    for i in dict:
        if i["match_id"] not in vetor.keys():
            vetor.update({(i["match_id"]):[i[j] for j in caracteristicas_partida]})
        vetor[i["match_id"]] = vetor[i["match_id"]] + [i[j] for j in caracteristicas_jogador]

    vetor =  list(vetor.values())
    return vetor"""

#x = list(script(caracteristicas_partida, caracteristicas_jogador))
#salvar("data.pk", x)

def selecionar_features(features_selecionados):
    caracteristicas_partida = ["radiant_win", "match_id", "game_mode", "start_time", "duration",
                               "first_blood_time", "radiant_score", "dire_score", "tower_status_radiant",
                               "tower_status_dire", "barracks_status_radiant", "barracks_status_dire"]
    caracteristicas_jogador = ["hero_id", "level", "player_slot", "account_id", "assists", "gold_per_min", "gold_spent",
                               "xp_per_min", "kills", "deaths", "last_hits"]

    indices_partida = []
    indices_jogador = []
    for i in features_selecionados:
        if i in caracteristicas_partida:
            indices_partida.append(caracteristicas_partida.index(i))
        if i in caracteristicas_jogador:
            indices_jogador.append(caracteristicas_jogador.index(i))

    x = ler('data_01.pk')

    dataset = []
    jogador = []
    for i in x:
        partida = [i[j] for j in indices_partida]
        
        indice = 12
        vetor_jogador = []
        n_jogadores = int((len(i) - 12) / 11)
        for x in range(n_jogadores):
            vetor_jogador = vetor_jogador + [i[indice+j] for j in indices_jogador]
            indice = indice + 11

        dataset.append([partida,vetor_jogador])
    return dataset

#x = ler('data.pk')
def normalizando(x):
    novo = []
    for i in x:
        novo.append([])
        if i[0] is True:
           novo[-1].append(1)
        else:
            novo[-1].append(0)

        for j in range(1,12):
            novo[-1].append(i[j])
        n_jogadores = int((len(i) - 12) / 11)
        indice = 12
        for j in range(n_jogadores):
            for x in range(indice, indice+2):
                novo[-1].append(i[x])

            if i[indice+2] < 128:
                novo[-1].append(1)
            else:
                novo[-1].append(0)
            for j in range(indice+3,indice+11):
                    novo[-1].append(i[j])
            indice = indice + 11
        salvar("data_02.pk", novo)
