## imports
from processo import Processo

## classes
class Processador:
    def __init__(self, id_processador) -> None:
        self.processo_atual = None
        self.id_processador = id_processador
        return

    def define_processo_atual(self, processo: Processo) -> None:
        self.processo_atual = processo
        print(f'Processo {processo.id_processo} foi atribuido ao Processador {self.id_processador}')
        return

    def executar(self) -> None:
        self.processo_atual.executando()
        print(f'Processo {self.processo_atual.id_processo} executando no processador {self.id_processador} com a política !!! definir !!!')
        return
