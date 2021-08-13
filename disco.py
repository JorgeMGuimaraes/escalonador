## imports
from processo import Processo, estado

estado_disco = {
    'idle': 0,
    'ocupado': 1
}

## classe

class Disco:
    def __init__(self, id_disco) -> None:
        self.id_disco   = id_disco
        # Refatorar, trocar esse estado por checar se processo is none, como no processador
        self.estado     = estado_disco['idle']
        self.processo_atual = None
        return

    def define_estado(self, novo_estado: int) -> None:
        self.estado = novo_estado
        return

    def disponivel(self) -> bool:
        return self.processo_atual == None

    def gravar(self) -> bool:
        if not self.disponivel():
            return True
        return False

    def define_processo_atual(self, processo: Processo) -> None:
        self.processo_atual = processo
        # TODO: ver se podemos remover esse print
        print(f'Disco {self.id} foi atribuido ao Processo {processo.id_processo}')
        return
    
    def pode_agregar(self, processo: Processo) -> bool:
        if self.processo_atual is None and processo.discos > 0:
            processo.discos     -= 1
            self.processo_atual = processo
            return True
        return False

    def liberar(self, processo: Processo):
        if self.processo_atual == processo:
            self.processo_atual = None
        return