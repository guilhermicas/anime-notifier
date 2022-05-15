"""
Verificar se o numero do EP guardado localmente é menor que o último que foi lançado:
    se sim mostrar notificação na barra de baixo
    ao clicar abrir link do último episódio
"""

import requests
from bs4 import BeautifulSoup
import re
import os

# File path to store the latest episode
FILEPATH = "/home/gui/.config/i3/scripts/OnePieceNotifier/eps.txt"


def checkStringInt(string: str):
    # Verifica se uma string pode ser convertida para int
    try:
        int(string)
        return True
    except ValueError:
        return False


def escreverFicheiroConfig():
    ultimo_ep_visto = 0
    # criar ficheiro e inserir ultimo EP
    with open(FILEPATH, "w+") as f:
        # TODO:janela para pedir o ultimo ep
        while(True):
            ultimo_ep_visto = input("Qual foi o ultimo ep que viu?")
            if(checkStringInt(ultimo_ep_visto)):
                f.write(ultimo_ep_visto+"\n"+"gaming")
                break

    return int(ultimo_ep_visto)


def corrigirFicheiroConfig():
    # se o ficheiro existir, eliminar
    # continuar com a configuração
    print("Ficheiro de registo de ultimo episódio mal configurado, a recriar")
    if os.path.isfile(FILEPATH):
        os.remove(FILEPATH)

    return escreverFicheiroConfig()


def fetchUltimoEpVisto():
    if not os.path.isfile(FILEPATH):
        print('Ficheiro não existe, a criar um novo ficheiro de configuração')

        return escreverFicheiroConfig()
    else:
        # Caso o ficheiro exista
        with open(FILEPATH, "r+") as f:
            conteudo = f.readlines()

        # se o ficheiro nao tiver nenhum registo
        if(not conteudo):
            print("Ficheiro de configuração vazio, a recriar")
            return corrigirFicheiroConfig()

        for line in conteudo:
            # Se o que tiver na linha nao for numero de episódio, entao recriar ficheiro de configuração
            if(not checkStringInt(line)):
                return corrigirFicheiroConfig()
            return int(line)


def fetchLastReleasedEP():
    html_doc = requests.get(
        "https://onepiece.fandom.com/wiki/One_Piece_Wiki")
    if(html_doc.status_code == 200):
        soup = BeautifulSoup(html_doc.content, 'html.parser')

        # Ultimo episódio que saiu
        ultimo_ep_released = int(soup.find_all("a", href=re.compile(
            "^\/wiki\/Episode_\d*$"), title=re.compile("^Episode \d*"))[0].string.split(" ")[1]
        )

        return ultimo_ep_released
    else:
        print("Não foi possivel verificar se saiu um novo episódio, verifique o estado da sua conexão ou o site onde se vai buscar a informação está Down")
        return -1


def updateLastEP(ep: int):
    with open(FILEPATH, 'r') as file:
        data = file.readlines()

    data[1] = str(ep)

    with open(FILEPATH, 'w') as file:
        file.writelines(data)


def checkIfNewEpisode():

    ultimo_ep_released = fetchLastReleasedEP()
    if(ultimo_ep_released == -1):
        quit()
    ultimo_episodio_visto = fetchUltimoEpVisto()

    # Inserir o ultimo episódio que saiu na segunda linha como CACHE para nao ter que estar sempre a fazer request ao servidor, se ouver ainda algum episódio para ver
    updateLastEP(ultimo_ep_released)

    # Se sair novo episódio mostrar notificação, ao clicar abrir na página
    if(ultimo_ep_released > ultimo_episodio_visto):
        return True
    else:
        return False


if __name__ == "__main__":
    if(checkIfNewEpisode()):
        print("T")

# TODO:
# Ao clicar na notificação:
# abrir neste link:
# novo_ep_link = "https://lite.animevibe.wtf/anime/one-piece/"+str(ultimo_ep)(CHECK)
# E incrementar ultimo_episodio_visto no ficheiro de configuração
