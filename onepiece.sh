#!/bin/bash

# bool que busca se falta ou não algum episódio para ver
faltaEpisodio=$(python /home/gui/.config/i3/scripts/OnePieceNotifier/app.py)

if [ $faltaEpisodio == "T" ]; then
  echo "(One☠️Piece)"
fi

site="https://lite.animevibe.wtf/anime/one-piece/"

#Ultimo episódio visto +1
ultimo_ep=$(($(cat /home/gui/.config/i3/scripts/OnePieceNotifier/ultimo_ep.cfg)+1))

case $BLOCK_BUTTON in
  1) firefox "${site}${ultimo_ep}"
esac

#TODO:
#Criar cache do ultimo episódio para nao tar sempre a fazer request(se ainda falta ao user ver episódio não vale a pena tar a fazer request)
#Incrementar ultimo ep visto por +1
