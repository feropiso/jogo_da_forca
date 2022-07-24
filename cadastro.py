import pygame
import dba
from pygame.locals import *
from sys import exit


class Cadastro:
    def __init__(self, menu):

        pygame.init()

        self.regis = dba
        self.menu = menu

        self.jogador = None
        self.nome_salvo = False
        self.clique_salvar = False

    def registroLoop(self):

        nome_usuario = ""

        run = True

        while run:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        nome_usuario = nome_usuario[0:-1]
                    else:
                        nome_usuario += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    #salvar
                    if 90 <= mouse[0] <= 190 and 160 <= mouse[1] <= 260:
                        if self.nome_salvo:
                            self.regis.addJogador(self.jogador)
                            self.menu.__init__(self.jogador)
                            self.menu.menuLoop()

                        else:
                            self.clique_salvar = True

                    #voltar
                    if 88 <= mouse[0] <= 122 and 318 <= mouse[1] <= 352:
                        self.menu.__init__("")
                        self.menu.menuLoop()

            mouse = pygame.mouse.get_pos()

            self.desenhaFormRegistro(mouse, nome_usuario)

            pygame.display.update()

    def desenhaFormRegistro(self, mouse, nome):

        self.menu.tela.fill(self.menu.vermelho)

        msg = self.menu.arial.render("Seu nome:", True, self.menu.preto)
        self.menu.tela.blit(msg, (90, 60))

        pygame.draw.rect(self.menu.tela, self.menu.branco, (90, 120, 514, 40), 0, 3)

        msg = self.menu.arial2.render(nome, True, self.menu.preto)
        self.menu.tela.blit(msg, (95, 125))

        self.jogador = nome

        if self.jogador != "":
            self.nome_salvo = True

        if self.clique_salvar:
            self.menu.mostraAlerta("Registre seu nome", 100, 250)

        self.menu.salvar()

        self.menu.voltar(mouse)
