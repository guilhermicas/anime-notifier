#!/bin/bash

site="https://animevibe.wtf/anime/one-piece/"
EPS="/home/gui/.config/i3/scripts/OnePieceNotifier/eps.txt"

ultimo_ep_visto=$(sed -n 1p $EPS)
ultimo_ep_released=$(sed -n 2p $EPS)

notificacaoEPNovo="<span face='Source Code Pro' size='small' weight='bold' foreground='#F8F840'>One☠️Piece</span>"

onClick() {
  # Só incrementa o ultimo episódio visto se o ultimo episodio visto for diferente do ultimo_ep_released
  if [ $(sed -n 1p $EPS) -ne $(sed -n 2p $EPS) ]; then
    proximoEpisodio=$((ultimo_ep_visto + 1));

    #Incrementar ultimo ep visto por +1 SE o utilizador clicar e abre firefox no site do anime
    sed -i "1s/.*/$(($(sed -n 1p $EPS) + 1))/" $EPS;
    firefox "${site}${proximoEpisodio}";
    echo ""
  fi
}

case $BLOCK_BUTTON in
  1) onClick;;
esac

#se for verdade quer dizer que saiu novo episodio
novo_ep_flag=false

if [ $ultimo_ep_released -eq $ultimo_ep_visto ]; then
  # bool que busca se falta ou não algum episódio para ver
  $(python "/home/gui/.config/i3/scripts/OnePieceNotifier/app.py");
  #faltaEpisodio=$(python /home/gui/.config/i3/scripts/OnePieceNotifier/app.py)
  ultimo_ep_vistol=$(sed -n 1p $EPS)
  ultimo_ep_releasedl=$(sed -n 2p $EPS)

  #atualizar ultimo ep released no ficheiro e os episodios forem diferentes fazer print

  #caso tenha detetado novo episodio dar set na flag de novo episodio lançado
  if [ $ultimo_ep_releasedl -gt $ultimo_ep_vistol ]; then
    echo $notificacaoEPNovo
  fi

elif [ $ultimo_ep_released -gt $ultimo_ep_visto ]; then
  echo $notificacaoEPNovo
fi

#maybe TODO:
#Mostrar current episode - last released episode
#So fazer a pesquisa de novo episodio quando chegar a domingo e ja ter visto episodio do domingo passado, para quando ver o episodio nao estar sempre a fazer requests, so quando chegar a domingo
#Se calhar dar track até proximo domingo enquanto nao chegarmos ao proximo domingo nao fazer a request porque de certeza que nao vai sair episodio e caso esteja atrasado como ainda nao viu e ainda nao registou o proximo domingo por ainda nao ter visto entao vai continuar a fazer requests
