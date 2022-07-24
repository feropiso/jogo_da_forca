import sqlite3


def criaBanco():

    cursor = criaConexao().cursor()

    # criando a tabela de jogadores
    cursor.execute("CREATE TABLE jogadores "
                   "(id_jogador INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nome VARCHAR(50) NOT NULL)")

    # criando a tabela de resultados
    cursor.execute("CREATE TABLE resultados (id_resultados INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                        "acertos INTEGER NOT NULL, erros INTEGER NOT NULL, palavra VARCHAR(50), "
                            "palavra_certa INTEGER NOT NULL, tempo VARCHAR(8), "
                                "saldo INTEGER NOT NULL, fk_jogador INTEGER NOT NULL)")

    # criando a tabela de personagens
    cursor.execute("CREATE TABLE personagens "
                   "(id_personagem INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, personagem INTEGER NOT NULL)")

    criaConexao().commit()

    criaConexao().close()

def criaConexao():
    conexao = sqlite3.connect("registro_de_jogadores.db")

    return conexao
