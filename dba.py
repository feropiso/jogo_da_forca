import banco

b = banco
con = b.criaConexao()
cursor = con.cursor()

def retornaNomeJogador(id):

    data = []

    for row in cursor.execute("SELECT nome FROM jogadores WHERE id_jogador='"+id+"'").fetchall():
        data.append(row)

    con.commit()

    return data

def retornaIdJogador(nome):

    data = []

    for row in cursor.execute("SELECT id_jogador FROM jogadores WHERE nome='"+nome+"'").fetchall():
        data.append(row)

    con.commit()

    return data

def addJogador(nome):

    if not retornaIdJogador(nome):
        cursor.execute("INSERT INTO jogadores (nome) VALUES ('"+nome+"')")

        con.commit()


def addResultados(acertos, erros, nome, palavra, palavra_certa, tempo, pontuacao):

    id = retornaIdJogador(nome)

    id = str(id[0][0])

    saldo = str(pontuacao)
    acertos = str(acertos)
    erros = str(erros)
    palavra_certa = str(palavra_certa)

    cursor.execute("INSERT INTO resultados (acertos, erros,  palavra, palavra_certa, tempo, saldo, fk_jogador)"
                   "VALUES ('"+acertos+"','"+erros+"','"+palavra+"','"+palavra_certa+"','"+tempo+"', '"+saldo+"','"+id+"')")

    con.commit()

def retornaResultadosTotais(jogadores):

    id = ""
    data = []
    cont = 0

    for jogador in jogadores:

        id = str(jogadores[cont][0])

        for row in cursor.execute("SELECT j.nome, sum(r.acertos), sum(r.erros), sum(r.saldo) FROM resultados as r "
                                  "INNER JOIN jogadores as j on j.id_jogador = r.fk_jogador WHERE r.fk_jogador='"+id+"'"):
            data.append(row)

        cont += 1

    data.sort(key=lambda x: x[3], reverse=True)

    return data

def retornaJogadores():

    data = []
    for row in cursor.execute("SELECT * FROM jogadores"):
        data.append(row)

    return data

def retornaUltimoRegistro():

    data = []

    for row in cursor.execute(
            "SELECT nome FROM jogadores WHERE id_jogador = (SELECT MAX( id_jogador ) FROM jogadores)"):
        data.append(row)

    return data

def addPersonagem(valor):

    valor = str(valor)

    cursor.execute("INSERT INTO personagens (personagem) VALUES ('"+valor+"')")

    con.commit()

def retornaUltimoPersonagem():

    data = []

    for row in cursor.execute(
            "SELECT personagem FROM personagens WHERE id_personagem = (SELECT MAX( id_personagem ) FROM personagens)"):
        data.append(row)

    return data

def retornaPersonagemMaisFrequente():

    data = []

    for row in cursor.execute("SELECT personagem, Count(*) FROM personagens GROUP BY personagem HAVING Count(*) > 1"):
        data.append(row)

    data.sort(key=lambda x: x[1], reverse=True)

    return data

def retornaPalavrasAcertadas(id):

    id = str(id)

    data = []
    for row in cursor.execute("SELECT DISTINCT palavra FROM resultados WHERE palavra_certa = 1 AND fk_jogador='"+id+"'"):
        data.append(row[0])

    return data



