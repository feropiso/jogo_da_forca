import pygame
import dba
from pygame.locals import *
from sys import exit


class Personagens:
    def __init__(self, menu, nome):

        pygame.init()

        self.menu = menu
        self.abd = dba
        self.nome = nome

        # personagens
        self.valor = 0
        self.preso = False
        self.preso1 = False
        self.preso2 = False
        self.person_selecionado = False

    def personagensLoop(self):

        run = True

        while run:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 92 <= mouse[0] <= 202 and 120 <= mouse[1] <= 260:
                        self.person_selecionado = True
                        self.preso = True
                        self.valor = 1

                    if 294 <= mouse[0] <= 404 and 120 <= mouse[1] <= 260:
                        self.person_selecionado = True
                        self.preso1 = True
                        self.valor = 2

                    if 496 <= mouse[0] <= 606 and 120 <= mouse[1] <= 260:
                        self.person_selecionado = True
                        self.preso2 = True
                        self.valor = 3

                    if self.person_selecionado:
                        # salvar
                        if 300 <= mouse[0] <= 400 and 300 <= mouse[1] <= 400:
                            self.abd.addPersonagem(self.valor)
                            self.menu.__init__(self.nome)
                            self.menu.menuLoop()

                    # voltar
                    if 88 <= mouse[0] <= 122 and 318 <= mouse[1] <= 352:
                        self.menu.__init__("")
                        self.menu.menuLoop()

            mouse = pygame.mouse.get_pos()

            self.desenhaOpcoesDePersonagem(mouse)

            pygame.display.update()

    def desenhaOpcoesDePersonagem(self, mouse):

        fundo = pygame.image.load("imagens/personagens.jpg")
        self.menu.tela.blit(fundo, (0, 0))

        caminho = ["imagens/prisioneiro/cabeca2.png", "imagens/prisioneiro1/cabeca2.png",
                   "imagens/prisioneiro2/cabeca2.png"]

        nome = ["Preso 894512", "Preso 123456", "Preso 789101"]

        if self.person_selecionado:

            msg = self.menu.arial.render("Seu personagem:", True, self.menu.preto)
            self.menu.tela.blit(msg, (270, 60))
            pygame.draw.rect(self.menu.tela, self.menu.branco, (294, 120, 110, 140), 0, 3)

            if self.preso:
                self.desenhaPreso(300, 124, 285, 270, caminho[0], nome[0])

            if self.preso1:
                self.desenhaPreso(300, 124, 285, 270, caminho[1], nome[1])

            if self.preso2:
                self.desenhaPreso(300, 124, 285, 270, caminho[2], nome[2])

            self.menu.voltar(mouse)
            self.salvarPersonagem()

        else:

            msg = self.menu.arial.render("Escolha seu personagem:", True, self.menu.preto)
            self.menu.tela.blit(msg, (245, 60))

            for i in range(3):
                if 92 + i * 202 <= mouse[0] <= 202 + i * 202 and 120 <= mouse[1] <= 260:
                    pygame.draw.rect(self.menu.tela, self.menu.azul, (92 + i * 202, 120, 110, 140), 0, 3)
                else:
                    pygame.draw.rect(self.menu.tela, self.menu.branco, (92 + i * 202, 120, 110, 140), 0, 3)

            self.desenhaPreso(95, 124, 85, 270, caminho[0], nome[0])
            self.desenhaPreso(300, 124, 290, 270, caminho[1], nome[1])
            self.desenhaPreso(500, 124, 490, 270, caminho[2], nome[2])

            self.menu.voltar(mouse)

    def desenhaPreso(self, x, y, z, w, caminho, nome):
        cabeca = pygame.image.load(caminho)
        self.menu.tela.blit(cabeca, (x, y))

        msg = self.menu.arial.render(nome, True, self.menu.preto)
        self.menu.tela.blit(msg, (z, w))

    def salvarPersonagem(self):
        s = pygame.image.load("imagens/salvar.png")
        self.menu.tela.blit(s, (300, 300))