## imports
from processo import Processo
from typing import List


class Escalonador:
    def __init__(self, processos: List[Processo]) -> None:
        self.processos = self.ordena_processos(processos)
        return
    
    ## carrega
    def ordena_processos(self, processos: List[Processo]) -> List[Processo]:
        return sorted(processos, key = lambda proc: (proc.chegada, proc.prioridade))

    ## usa
    def continuar_processando(self) -> bool:
        for processo in self.processos:
            if processo.estado < 100: return True

        return False

    def politica_fifo(self) -> None:

        return

    def politica_feedback(self) -> None:

        return
    
    ## exibe
    def imprime_processos_recebidos(self) -> None:
        for processo in self.processos:
            tempo = 'tempo real' if processo.prioridade == 0 else 'usuário'
            disco = 'sem necessidade de recursos de E/S' if processo.io == 0 else f'requer { processo.io} unidade de disco'
            print(f'Processo {processo.id_processo}: chegada no momento {processo.chegada}, prioridade {processo.prioridade} ({tempo}), duração de {processo.duracao} segundos de CPU e memória de {processo.memoria} MBytes, {disco}')
        return

    def imprime_andamento(self, quanta:int) -> None:
        espacamento = '    '
        s = 'Andamento:\n'
        s+= '                 |'
        for quantum in range(quanta + 1):
            s += f'{quantum:>2}|'
        print(f'{s}\n')

        for processo in self.processos:
            s = f'{espacamento}Processo {processo.id_processo:>2}: |'
            for processou in processo.andamento:
                s += '* |' if processou else '  |'
            print(f'{s}\n')
        return
