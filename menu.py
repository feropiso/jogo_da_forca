import pygame
import dba
from pygame.locals import *
from sys import exit
from jogo import Jogo
from estatisticas import Estatisticas
from cadastro import Cadastro
from personagens import Personagens


class Menu:
    def __init__(self, nome):

        #configurações do jogo
        pygame.init()
        pygame.display.set_caption("Super Forca 2000")

        #definindo tamanho
        self.largura_tela = 700
        self.altura_tela = 490
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))

        #definindo cores
        self.branco = (255, 255, 255)
        self.azul = (0, 132, 232)
        self.preto = (0, 0, 0)
        self.vermelho = (137, 28, 36)
        self.cinza = (128, 128, 128)
        self.laranja = (242, 79, 0)
        self.marrom = (150, 75, 0)
        self.verde = (0, 100, 0)

        #definindo fontes
        self.arial = pygame.font.SysFont("arial", 25, True)  # fonte, tamanho, negrito, itálico
        self.arial1 = pygame.font.SysFont("arial", 35, True)
        self.arial2 = pygame.font.SysFont("arial", 20, True)
        self.arial3 = pygame.font.SysFont("arial", 20)

        #definindo variáveis
        self.adm = dba
        self.cad = Cadastro(self)
        self.jogo = Jogo(self, 0, "")
        self.estatisticas = Estatisticas()
        self.personagens = Personagens(self, nome)

        self.jogador = nome
        self.rodando = True
        self.nome_salvo = False
        self.clique_inicio = False
        self.personagem_escolhido = False

        self.personagem_salvo = False

    def menuLoop(self):

        self.personagem_escolhido = self.adm.retornaUltimoPersonagem()

        if self.personagem_escolhido:
            self.personagem_salvo = True

        if self.jogador != "":
            self.nome_salvo = True

        run = True

        while run:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if 260 <= mouse[0] <= 440 and 65 <= mouse[1] <= 95:
                        self.__init__(self)
                        self.cad.registroLoop()

                    if 260 <= mouse[0] <= 440 and 155 <= mouse[1] <= 185:
                        self.estatisticas.__int__(self)
                        self.estatisticas.estatisticasLoop()

                    if 260 <= mouse[0] <= 440 and 245 <= mouse[1] <= 275:
                        self.personagens.__init__(self, self.jogador)
                        self.personagens.personagensLoop()

                    if 300 <= mouse[0] <= 400 and 355 <= mouse[1] <= 385:

                        if self.personagem_salvo and self.nome_salvo:
                            self.jogo.__init__(self, self.personagem_escolhido[0][0], self.jogador)
                            self.jogo.jogoLoop()

                        else:
                            self.clique_inicio = True

            mouse = pygame.mouse.get_pos()

            self.desenhaMenu(mouse)

            pygame.display.update()

    def desenhaMenu(self, mouse):

        fundo = pygame.image.load("imagens/fundo_menu.jpg")
        self.tela.blit(fundo, (0, 0))

        #botão para registro
        if 260 <= mouse[0] <= 440 and 65 <= mouse[1] <= 95:
            pygame.draw.rect(self.tela, self.azul, (260, 65, 180, 30), 0, 3)
        else:
            pygame.draw.rect(self.tela, self.branco, (260, 65, 180, 30), 0, 3)

        msg = self.arial.render("REGISTRE-SE", True, self.preto)
        self.tela.blit(msg, (275, 65))

        #botão para mostrar as estatísticas
        if 260 <= mouse[0] <= 440 and 155 <= mouse[1] <= 185:
            pygame.draw.rect(self.tela, self.azul, (260, 155, 180, 30), 0, 3)
        else:
            pygame.draw.rect(self.tela, self.branco, (260, 155, 180, 30), 0, 3)

        msg = self.arial.render("ESTATÍSTICAS", True, self.preto)
        self.tela.blit(msg, (275, 155))

        #botão para mostrar personagem
        if 260 <= mouse[0] <= 440 and 245 <= mouse[1] <= 275:
            pygame.draw.rect(self.tela, self.azul, (260, 245, 180, 30), 0, 3)
        else:
            pygame.draw.rect(self.tela, self.branco, (260, 245, 180, 30), 0, 3)

        msg = self.arial.render("PERSONAGENS", True, self.preto)
        self.tela.blit(msg, (270, 245))

        #botão pra iniciar o jogo
        if 300 <= mouse[0] <= 400 and 355 <= mouse[1] <= 385:
            pygame.draw.rect(self.tela, self.azul, (300, 355, 100, 30), 0, 3)
        else:
            pygame.draw.rect(self.tela, self.branco, (300, 355, 100, 30), 0, 3)

        msg = self.arial.render("INICIAR", True, self.preto)
        self.tela.blit(msg, (310, 355))

        if self.clique_inicio:
            self.mostraAlerta("Falta o personagem e o seu cadastro!", 200, 400)

    def voltar(self, mouse):
        seta = pygame.image.load("imagens/seta.png")
        self.tela.blit(seta, (90, 320))

        if 88 <= mouse[0] <= 122 and 318 <= mouse[1] <= 352:
            pygame.draw.rect(self.tela, self.preto, (88, 318, 34, 34), 2, 3)

    def salvar(self):
        s = pygame.image.load("imagens/salvar.png")
        self.tela.blit(s, (90, 160))

    def mostraAlerta(self, msg, x, y):

        msg = self.arial2.render(msg, True, self.vermelho)
        self.tela.blit(msg, (x, y))

