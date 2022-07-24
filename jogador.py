
class Jogador:
    def __init__(self):
        self.erros = None
        self.acertos = None
        self.nome = None
        self.palavra = None
        self.palavra_acertada = None
        self.tempo = None

    def setNome(self, nome):
         self.nome = nome

    def setAcertos(self, acertos):
        self.acertos = acertos

    def setErros(self, erros):
        self.erros = erros

    def getNome(self):
        return self.nome

    def getAcertos(self):
        return self.acertos

    def getErros(self):
        return self.erros

    def setPalavra(self, p):
         self.palavra = p

    def setPalavra_Acertada(self, pc):
        self.palavra_acertada = pc

    def setTempo(self, t):
        self.tempo = t

    def getPalavra(self):
        return self.palavra

    def getPalavra_Acertada(self):
        return self.palavra_acertada

    def getTempo(self):
        return self.tempo
