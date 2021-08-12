## imports
from processo import Processo

## classes
class Processador:
    def __init__(self, id_processador) -> None:
        self.processos      = []
        self.processo_atual = None
        self.id_processador = id_processador
        return
    
    def adiciona_processo(self, processo: Processo) -> None:
        self.processos.append(processo)
        return

    def define_processo_atual(self, processo: Processo) -> None:
        self.processo_atual = processo
        print(f'Processo {processo.id_processo} foi atribuido ao Processador {self.id_processador}')
        return

    def executar(self, politica) -> None:
        politica(self.processo_atual)
        return