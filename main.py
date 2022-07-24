import banco
from menu import Menu


def iniciaBD():

    b = banco

    try:
        b.criaBanco()

    except:
        print("Banco já criado.")


def principal():

    m = Menu("")

    while m.rodando:
        m.menuLoop()
        m.menu.jogoLoop()


if __name__ == '__main__':
    iniciaBD()
    principal()