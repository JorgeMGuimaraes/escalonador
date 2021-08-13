## imports
from processo import Processo, estado

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

    def pode_executar(self) -> bool:
        if self.processo_atual is not None:
            self.processo_atual.executando()
            #print(f'Processo {self.processo_atual.id_processo} executando no processador {self.id_processador} com a política !!! definir !!!')
            return True
        return False
    
    def pode_agregar(self, processo: Processo) -> bool:
        if self.processo_atual is None:
            processo.atualiza_estado(estado['executando'])
            self.processo_atual = processo
            return True
        return False

    def liberar(self, processo: Processo):
        if self.processo_atual == processo:
            self.processo_atual = None
        return