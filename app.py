"""
Verificar se o numero do EP guardado localmente é menor que o último que foi lançado:
    se sim mostrar notificação na barra de baixo
    ao clicar abrir link do último episódio
"""

import requests
from bs4 import BeautifulSoup
import re

html_doc = requests.get(
    "https://onepiece.fandom.com/wiki/One_Piece_Wiki")

if(html_doc.status_code == 200):
    soup = BeautifulSoup(html_doc.content, 'html.parser')

    ultimo_ep = soup.find_all("a", href=re.compile(
        "^\/wiki\/Episode_\d*$"), title=re.compile("^Episode \d*"))[0].string.split(" ")[1]
