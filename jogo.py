import pygame
from pygame.locals import *
from sys import exit
from vencedor import Vencedor
import random
import jogador
import dba
import datetime


class Jogo:
    def __init__(self, menu, valor, nome):

        pygame.init()

        self.menu = menu
        self.valor = valor
        self.nome = nome

        self.adm = dba
        self.player = jogador

        self.tempo_atual = datetime.datetime.now()
        self.minutos = "00"
        self.tempo = None

        self.dica = None
        self.acertos = None
        self.letra_usuario = None
        self.jogada_usuario = None

        self.jogando = True
        self.perdeu = False
        self.venceu = False

        self.erros = 0
        self.pontuacao = 0

        #personagens
        self.preso = False
        self.preso1 = False
        self.preso2 = False

        #Zeramento
        self.final = False
        self.vencedor = Vencedor(self.menu, "")

        self.palavra = self.carregaPalavra()
        self.lista = self.mostraCamposVazios()
        self.lista_tentativas = []

    def jogoLoop(self):

        while self.jogando:

            RELOGIO = pygame.time.Clock()
            FPS = 45

            RELOGIO.tick(FPS)

            letra_recebida = self.menu.arial.render(self.letra_usuario, True, self.menu.preto)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    self.letra_usuario = event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 220 <= mouse[0] <= 245 and 35 <= mouse[1] <= 55:
                        self.jogada_usuario = self.recebeJogada(self.letra_usuario)

                        if self.jogada_usuario not in self.lista_tentativas:
                            self.lista_tentativas.append(self.jogada_usuario)

                        self.contaErros()

                    if self.perdeu or self.venceu:
                        if 350 <= mouse[0] <= 400 and 290 <= mouse[1] <= 340: #Clique -> reinicia o jogo
                            self.salvaResultados()
                            self.menu.__init__("")
                            self.menu.menuLoop()

                        if 430 <= mouse[0] <= 480 and 290 <= mouse[1] <= 340: #Clique -> fecha o jogo
                            self.salvaResultados()
                            pygame.quit()
                            exit()

            mouse = pygame.mouse.get_pos()

            if self.erros == 6:
                self.perdeu = True
                self.player.Jogador.setPalavra_Acertada(self, 0)

            self.desenhaJogo(mouse)

            if not self.perdeu and not self.venceu:
                self.menu.tela.blit(letra_recebida, (195, 30))

                msg = self.menu.arial.render("Letras digitadas:", True, self.menu.preto)
                self.menu.tela.blit(msg, (470, 110))

                self.mostraTentativas()

            self.desenhaForca()
            self.preencheJogadaCorreta()

            pygame.display.update()

    def desenhaJogo(self, mouse):

        if self.valor == 1:
            self.preso = True

        if self.valor == 2:
            self.preso1 = True

        if self.valor == 3:
            self.preso2 = True

        fundo = pygame.image.load("imagens/fundo.jpg")
        self.menu.tela.blit(fundo, (0, 0))

        if not self.perdeu and not self.venceu:
            letras_total = len(self.palavra)
            letras_faltando = self.lista.count('_')
            self.acertos = letras_total - letras_faltando

            msg = self.menu.arial.render("Digite sua letra: ", True, self.menu.preto)
            self.menu.tela.blit(msg, (30, 30))

            msg = self.menu.arial.render(self.dica, True, self.menu.preto)
            self.menu.tela.blit(msg, (300, 445))

            msg = self.menu.arial.render("Acertos: ", True, self.menu.preto)
            self.menu.tela.blit(msg, (470, 30))

            msg = str(self.acertos)+" / "+str(letras_total)
            msg = self.menu.arial.render(msg, True, self.menu.preto)
            self.menu.tela.blit(msg, (590, 30))

            msg = self.menu.arial.render("Tentativas: ", True, self.menu.preto)
            self.menu.tela.blit(msg, (470, 70))

            msg = str(self.erros) + " / " + str(6)
            msg = self.menu.arial.render(msg, True, self.menu.preto)
            self.menu.tela.blit(msg, (590, 70))

            if 220 <= mouse[0] <= 245 and 35 <= mouse[1] <= 55:
                pygame.draw.rect(self.menu.tela, self.menu.cinza, (220, 35, 25, 20), 0, 3)#0->preenchido; 3->cantos arredondados
                pygame.draw.circle(self.menu.tela, self.menu.preto, (232, 45), 5, 0)
            else:
                pygame.draw.rect(self.menu.tela, self.menu.preto, (220, 35, 25, 20), 0, 3)
                pygame.draw.circle(self.menu.tela, self.menu.cinza, (232, 45), 5, 0)

            tempo = datetime.datetime.now()

            tempo_aux = tempo - self.tempo_atual

            segundos = tempo_aux.seconds

            if segundos >= 59:
                self.minutos = segundos.real // 60

                if self.minutos <= 9:
                    self.minutos = "0" + str(self.minutos)

                segundos = segundos.real % 60

            if segundos <= 9:
                segundos = "0"+str(segundos)

            msg = str(self.minutos)+" : " +str(segundos)
            self.tempo = msg
            msg = self.menu.arial.render(msg, True, self.menu.vermelho)
            self.menu.tela.blit(msg, (320, 20))

        if self.venceu:
            self.processaVencedor()
            self.desenhaReinicioDeJogo(mouse)

        if self.perdeu:
            self.processaPerdedor()
            self.desenhaReinicioDeJogo(mouse)

        self.player.Jogador.setAcertos(self, self.acertos)
        self.player.Jogador.setErros(self, self.erros)
        self.player.Jogador.setTempo(self, self.tempo)


    def preencheJogadaCorreta(self):

        indice = 0
        v = len(self.palavra) + 2
        l = self.menu.largura_tela / v

        for i in range(len(self.palavra)):
            pos_lista = self.menu.arial.render(self.lista[i].upper(), True, self.menu.preto)
            self.menu.tela.blit(pos_lista, (l * (i + 1) + i * 5, 400))

        for letra in self.palavra:
            if self.jogada_usuario == letra:
                self.lista[indice] = letra
            indice += 1

        if "_" not in self.lista:
            self.venceu = True
            self.player.Jogador.setPalavra_Acertada(self, 1)

    def carregaPalavra(self):

        palavras = []

        with open("palavras.txt", "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                palavras.append(linha)

        sorteio = 0

        retorno = self.verificaZeramento(palavras)

        if len(retorno) == 1:
            self.final = True
            palavra_escolhida = retorno[0].upper()

            for i in range(len(palavras)):
                if palavras[i].upper() == palavra_escolhida:
                    sorteio = i
                    break
        else:
            sorteio = random.randrange(0, len(palavras))
            palavra_escolhida = palavras[sorteio].upper()

        self.player.Jogador.setPalavra(self, palavra_escolhida)

        self.processaDica(sorteio)

        return palavra_escolhida

    def mostraCamposVazios(self):
        lista = []

        for letra in self.palavra:
            lista.append("_")

        return lista

    def contaErros(self):

        if self.jogada_usuario not in self.palavra:
            self.erros += 1

    def desenhaForca(self):

        self.desenhaPatibulo()

        if self.erros == 1:
            self.desenhaCabeca()

        if self.erros == 2:
            self.desenhaCabeca()
            self.desenhaTronco()

        # Desenha as pernas
        if self.erros == 3:
            self.desenhaCabeca()
            self.desenhaTronco()
            self.desenhaPernaDireita()

        if self.erros == 4:
            self.desenhaCabeca()
            self.desenhaTronco()
            self.desenhaPernaDireita()
            self.desenhaPernaEsquerda()

        #Desenha os braços
        if self.erros == 5:
            self.desenhaCabeca()
            self.desenhaTronco()
            self.desenhaPernaDireita()
            self.desenhaPernaEsquerda()
            self.desenhaBracoDireito()

        if self.erros == 6:
            self.desenhaCabeca()
            self.desenhaTronco()
            self.desenhaPernaDireita()
            self.desenhaPernaEsquerda()
            self.desenhaBracoDireito()
            self.desenhaBracoEsquerdo()

    def recebeJogada(self, l):
        jogada = l.strip().upper()
        return jogada

    def desenhaPatibulo(self):
        # Desenha a forca
        pygame.draw.rect(self.menu.tela, self.menu.marrom, (30, 90, 20, 300))
        pygame.draw.rect(self.menu.tela, self.menu.marrom, (20, 90, 200, 20))
        pygame.draw.line(self.menu.tela, self.menu.preto, (35, 110), (35, 380))
        pygame.draw.line(self.menu.tela, self.menu.preto, (40, 110), (40, 380))
        pygame.draw.line(self.menu.tela, self.menu.preto, (45, 110), (45, 380))
        pygame.draw.rect(self.menu.tela, self.menu.marrom, (175, 110, 5, 20))
        pygame.draw.circle(self.menu.tela, self.menu.marrom, (177, 145), 15, 4)

    def desenhaCabeca(self):

        msg = ""

        if self.preso:
            msg = "imagens/prisioneiro/cabeca.png"

        if self.preso1:
            msg = "imagens/prisioneiro1/cabeca.png"

        if self.preso2:
            msg = "imagens/prisioneiro2/cabeca.png"

        cabeca = pygame.image.load(msg)

        self.menu.tela.blit(cabeca, (160, 115))

    def desenhaTronco(self):
        tronco = pygame.image.load("imagens/prisioneiro/tronco.png")
        self.menu.tela.blit(tronco, (148, 165))

    def desenhaPernaDireita(self):
        perna_direita = pygame.image.load("imagens/prisioneiro/perna_direita.png")
        self.menu.tela.blit(perna_direita, (184, 266))

    def desenhaPernaEsquerda(self):
        perna_direita = pygame.image.load("imagens/prisioneiro/perna_esquerda.png")
        self.menu.tela.blit(perna_direita, (140, 266))

    def desenhaBracoDireito(self):
        braco_direito = pygame.image.load("imagens/prisioneiro/braco_direito.png")
        self.menu.tela.blit(braco_direito, (210, 172))

    def desenhaBracoEsquerdo(self):
        braco_esquerdo = pygame.image.load("imagens/prisioneiro/braco_esquerdo.png")
        self.menu.tela.blit(braco_esquerdo, (128, 172))

    def processaDica(self, sorteio):

        if 0 <= sorteio <= 9:
            self.dica = "É um animal."

        elif 10 <= sorteio <= 19:
            self.dica = "É um objeto."

        elif 20 <= sorteio <= 29:
            self.dica = "É um esporte."

        elif 30 <= sorteio <= 39:
            self.dica = "É um fenômeno da natureza."

        elif 40 <= sorteio <= 49:
            self.dica = "É um time."

        elif 50 <= sorteio <= 59:
            self.dica = "É um (a) deus (a) grego (a)."

        elif 60 <= sorteio <= 69:
            self.dica = "É um (a) escritor (a)."

        elif 70 <= sorteio <= 79:
            self.dica = "É um (a) pintor (a)."

        elif 80 <= sorteio <= 89:
            self.dica = "É uma cidade."

        else:
            self.dica = "É um país."

    def processaVencedor(self):

        if self.final and self.venceu:
            self.vencedor.__init__(self.menu, self.nome)
            self.vencedor.vencedorLoop()
        else:
            msg = ""

            if self.preso:
                msg = "Parabéns, você salvou o preso 894512!"

            if self.preso1:
                msg = "Parabéns, você salvou o preso 123456!"

            if self.preso2:
                msg = "Parabéns, você salvou o preso 789101!"

            vencedor = self.menu.arial.render(msg, True, self.menu.azul)
            self.menu.tela.blit(vencedor, (30, 30))

    def processaPerdedor(self):

        msg = ""

        if self.preso:
            msg = "O preso 894512 morreu!"

        if self.preso1:
            msg = "O preso 123456 morreu!"

        if self.preso2:
            msg = "O preso 789101 morreu!"

        msg = self.menu.arial.render(msg, True, self.menu.vermelho)
        self.menu.tela.blit(msg, (30, 30))
        msg = self.menu.arial.render("A palavra era: ", True, self.menu.preto)
        self.menu.tela.blit(msg, (280, 30))
        msg = self.menu.arial.render(self.palavra, True, self.menu.preto)
        self.menu.tela.blit(msg, (420, 30))

    def desenhaReinicioDeJogo(self, mouse):

        self.calculaPontuacao()

        self.mostraResultados()

        msg = self.menu.arial.render("Deseja tentar de novo?", True, self.menu.preto)
        self.menu.tela.blit(msg, (300, 250))

        if 350 <= mouse[0] <= 400 and 290 <= mouse[1] <= 340:
            pygame.draw.rect(self.menu.tela, self.menu.cinza, (350, 290, 50, 50), 0, 3)
        else:
            pygame.draw.rect(self.menu.tela, self.menu.branco, (350, 290, 50, 50), 0, 3)

        if 430 <= mouse[0] <= 480 and 290 <= mouse[1] <= 340:
            pygame.draw.rect(self.menu.tela, self.menu.cinza, (430, 290, 50, 50), 0, 3)
        else:
            pygame.draw.rect(self.menu.tela, self.menu.branco, (430, 290, 50, 50), 0, 3)

        msg = self.menu.arial.render("SIM", True, self.menu.preto)
        self.menu.tela.blit(msg, (355, 300))

        msg = self.menu.arial.render("NÃO", True, self.menu.preto)
        self.menu.tela.blit(msg, (433, 300))

    def mostraResultados(self):
        pygame.draw.rect(self.menu.tela, self.menu.branco, (350, 80, 200, 125), 0, 3)

        msg = self.menu.arial2.render("Pontuacao:", True, self.menu.preto)
        self.menu.tela.blit(msg, (354, 82))

        if self.pontuacao < 0:
            cor = self.menu.vermelho
        elif self.pontuacao > 0:
            cor = self.menu.verde
        else:
            cor = self.menu.azul

        msg = self.menu.arial2.render(str(self.pontuacao), True, cor)
        self.menu.tela.blit(msg, (454, 82))

        msg = self.menu.arial2.render("Acertos:", True, self.menu.preto)
        self.menu.tela.blit(msg, (354, 112))
        msg = self.menu.arial2.render(str(self.player.Jogador.getAcertos(self)), True, self.menu.verde)
        self.menu.tela.blit(msg, (454, 112))

        msg = self.menu.arial2.render("Erros:", True, self.menu.preto)
        self.menu.tela.blit(msg, (354, 142))
        msg = self.menu.arial2.render(str(self.player.Jogador.getErros(self)), True, self.menu.vermelho)
        self.menu.tela.blit(msg, (454, 142))

        msg = self.menu.arial2.render("Tempo:", True, self.menu.preto)
        self.menu.tela.blit(msg, (354, 172))
        msg = self.menu.arial2.render(self.player.Jogador.getTempo(self), True, self.menu.laranja)
        self.menu.tela.blit(msg, (454, 172))

    def salvaResultados(self):

        self.player.Jogador.setNome(self, self.nome)

        self.adm.addJogador(self.player.Jogador.getNome(self))

        self.adm.addResultados(self.player.Jogador.getAcertos(self),
                                    self.player.Jogador.getErros(self),
                                        self.player.Jogador.getNome(self),
                                            self.player.Jogador.getPalavra(self),
                                                self.player.Jogador.getPalavra_Acertada(self),
                                                    self.player.Jogador.getTempo(self), self.pontuacao)

    def mostraTentativas(self):

        for i in range(len(self.lista_tentativas)):

            msg = self.menu.arial2.render(self.lista_tentativas[i], True, self.menu.laranja)
            self.menu.tela.blit(msg, (470+i*15, 150))

    def calculaPontuacao(self):

        #palavra certa = 120 pts; palavra errada = 120; letra certa = 10 pts;
        #letra errada = -10 pts; minuto passado = -10 pts
        if self.player.Jogador.getPalavra_Acertada(self) == 1:
            acerto = 120
        else:
            acerto = -120

        eficacia = self.player.Jogador.getAcertos(self) - self.player.Jogador.getErros(self)

        time = self.player.Jogador.getTempo(self)

        eficiencia = int(time[0:2]) * 10 + int((int(time[5:]) / 60) * 10)

        self.pontuacao = (acerto + eficacia*10) - eficiencia

    def verificaZeramento(self, lista):

        id = self.adm.retornaIdJogador(self.nome)

        palavras_certas = []

        if id:
            palavras_certas = self.adm.retornaPalavrasAcertadas(id[0][0])

        restante = []

        for i in range(len(lista)):
            if lista[i].upper() not in palavras_certas:
                restante.append(lista[i])

        return restante
