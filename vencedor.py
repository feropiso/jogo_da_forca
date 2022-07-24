import pygame
import dba
from pygame.locals import *
from sys import exit


class Vencedor:
    def __init__(self, menu, nome):

        pygame.init()

        self.nome = nome
        self.db = dba
        self.menu = menu

    def vencedorLoop(self):

        run = True

        while run:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

            self.desenhaZeramento()

            pygame.display.update()

    def desenhaZeramento(self):

        fundo = pygame.image.load("imagens/fundo_vencedor.jpg")
        self.menu.tela.blit(fundo, (0, 0))

        trofeu = pygame.image.load("imagens/trofeu.png")
        self.menu.tela.blit(trofeu, (100, 100))

        pygame.draw.rect(self.menu.tela, self.menu.branco, (193, 28, 300, 45), 0, 3)
        pygame.draw.rect(self.menu.tela, self.menu.branco, (128, 428, 440, 40), 0, 3)

        msg = self.menu.arial1.render("Parabéns, "+self.nome+"!", True, self.menu.laranja)
        self.menu.tela.blit(msg, (195, 30))

        msg = self.menu.arial1.render("Você zerou o Super Forca 2000!", True, self.menu.laranja)
        self.menu.tela.blit(msg, (130, 430))

