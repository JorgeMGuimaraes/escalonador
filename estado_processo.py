## imports
from processo import Processo
from typing import List

## classes
class EstadoProcesso:
    def __init__(self, atual: List[Processo], proximo: List[Processo], estado:int, msg_padrao: str) -> None:
        self.atual      = atual
        self.proximo    = proximo
        self.msg_padrao = msg_padrao
        self.estado     = estado
        return

    def neste(self, processo: Processo):
        self.proximo.append(processo)
        self.atual.remove(processo)
        processo.estado = self.estado
        return self.msg_padrao