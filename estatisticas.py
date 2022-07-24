import pygame
import dba
from pygame.locals import *
from sys import exit


class Estatisticas:
    def __int__(self, menu):

        pygame.init()

        self.menu = menu
        self.registro = dba

    def estatisticasLoop(self):

        run = True

        while run:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # voltar
                    if 88 <= mouse[0] <= 122 and 318 <= mouse[1] <= 352:
                        self.menu.__init__("")
                        self.menu.menuLoop()

            mouse = pygame.mouse.get_pos()

            self.desenhaEstatistica(mouse)

            pygame.display.update()

    def desenhaEstatistica(self, mouse):

        self.menu.tela.fill(self.menu.azul)

        jogadores = self.registro.retornaJogadores()

        resultados = self.registro.retornaResultadosTotais(jogadores)

        msg = self.menu.arial.render("Estatísticas:", True, self.menu.preto)
        self.menu.tela.blit(msg, (295, 60))

        pygame.draw.rect(self.menu.tela, self.menu.branco, (100, 120, 514, 170), 0, 3)

        msg = self.menu.arial2.render("Ranking", True, self.menu.preto)
        self.menu.tela.blit(msg, (110, 120))

        pygame.draw.line(self.menu.tela, self.menu.preto, (110, 150), (590, 150))

        msg = self.menu.arial3.render("Acertos", True, self.menu.preto)
        self.menu.tela.blit(msg, (260, 150))

        msg = self.menu.arial3.render("Erros", True, self.menu.preto)
        self.menu.tela.blit(msg, (360, 150))

        msg = self.menu.arial3.render("Pontuação", True, self.menu.preto)
        self.menu.tela.blit(msg, (460, 150))

        if not resultados:
            msg = self.menu.arial3.render("Não há registro!", True, self.menu.vermelho)
            self.menu.tela.blit(msg, (260, 200))

        else:
            cont = 0
            for j in jogadores:

                pos = 1

                msg = str(pos + cont) + "° " + str(resultados[cont][0])
                msg = self.menu.arial3.render(msg, True, self.menu.preto)
                self.menu.tela.blit(msg, (120, 175 + 30 * cont))

                msg = str(resultados[cont][1])
                msg = self.menu.arial2.render(msg, True, self.menu.preto)
                self.menu.tela.blit(msg, (280, 175 + 30 * cont))

                msg = str(resultados[cont][2])
                msg = self.menu.arial2.render(msg, True, self.menu.preto)
                self.menu.tela.blit(msg, (380, 175 + 30 * cont))

                res = resultados[cont][3]

                if res < 0:
                    cor = self.menu.vermelho
                elif res > 0:
                    cor = self.menu.verde
                else:
                    cor = self.menu.azul

                msg = str(res)
                msg = self.menu.arial2.render(msg, True, cor)
                self.menu.tela.blit(msg, (480, 175 + 30 * cont))

                cont += 1

                if cont == 3:
                    break

            self.desenhaPersonagemMaisFrequente()

        self.menu.voltar(mouse)

    def desenhaPersonagemMaisFrequente(self):

        personagem_popular = self.registro.retornaPersonagemMaisFrequente()

        msg = self.menu.arial2.render("Personagem mais escolhido:", True, self.menu.preto)
        self.menu.tela.blit(msg, (180, 320))

        if personagem_popular:

            if personagem_popular[0][0] == 1:
                cabeca = pygame.image.load("imagens/prisioneiro/cabeca.png")
                self.menu.tela.blit(cabeca, (440, 305))

                msg = self.menu.arial2.render("Preso 894512", True, self.menu.preto)
                self.menu.tela.blit(msg, (410, 360))

            elif personagem_popular[0][0] == 2:
                cabeca = pygame.image.load("imagens/prisioneiro1/cabeca.png")
                self.menu.tela.blit(cabeca, (440, 305))

                msg = self.menu.arial2.render("Preso 123456", True, self.menu.preto)
                self.menu.tela.blit(msg, (410, 360))

            else:
                cabeca = pygame.image.load("imagens/prisioneiro2/cabeca.png")
                self.menu.tela.blit(cabeca, (440, 305))

                msg = self.menu.arial2.render("Preso 789101", True, self.menu.preto)
                self.menu.tela.blit(msg, (410, 360))

            msg = self.menu.arial2.render(str(personagem_popular[0][1])+" vezes", True, self.menu.preto)
            self.menu.tela.blit(msg, (530, 320))

