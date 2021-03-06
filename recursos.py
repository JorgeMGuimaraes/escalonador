## imports
# TODO: procurar por _typeshed em todos os arquivos
from processo import Processo
from disco          import Disco, estado_disco
from processador    import Processador
from typing         import List

class Recursos:
    """O sistema possui os seguintes recursos:
        * quatro CPUs
        * quatro discos
        * 16GB de memória principal
    """
    def __init__(self, cpus, discos, memoria) -> None:
        self.processadores  = self.carrega_processadores(cpus)
        self.discos         = self.carrega_discos(discos)
        self.memoria_total  = memoria
        self.memoria_uso    = 0
        return

    ## carrega
    def carrega_processadores(self, quantidade: int) -> List[Processador]:
        processadores = []
        for i in range(quantidade):
            processadores.append(Processador(i))
        return processadores

    def carrega_discos(self, quantidade: int) -> List[Disco]:
        discos = []
        for i in range(quantidade):
            discos.append(Disco(i))
        return discos
    ## usa
    def ha_memoria_disponivel(self, processo: Processo) -> bool:
        return self.memoria_total - self.memoria_uso > processo.memoria

    def ha_discos_disponiveis(self) -> bool:
        for disco in self.discos:
            if disco.disponivel():
                return True
        return False

    # TODO: [obsoleto]
    def ha_recursos_disponiveis(self, processo: Processo) -> bool:
        discos_disponiveis = 0
        for disco in self.discos:
            if disco.disponivel():
                discos_disponiveis += 1
        return (self.memoria_total - self.memoria_uso > processo.memoria) and (discos_disponiveis > processo.discos)

    def usa_memoria(self, quantidade: int) -> None:
        self.memoria_uso    += quantidade
        return

    def libera_memoria(self, thread: Processo) -> None:
        self.memoria_uso    -= thread.memoria
        return

    ## exibe
    def memoria_disponivel(self) -> int:
        return self.memoria_total - self.memoria_uso

    def imprime_processadores(self) -> None:
        for processador in self.processadores:
            atual = 'Idle' if processador.processo_atual is None else f'Processo {processador.processo_atual.id_processo}'
            print(f'Processador {processador.id_processador}: {atual}')
        return

    def imprime_memoria(self) -> None:
        print(f'Memória em uso:     {self.memoria_uso:>8}MB')
        print(f'Memória disponível: {self.memoria_disponivel():>8}MB')
        print(f'Memória total:      {self.memoria_total:>8}MB')
        return

    def imprime_discos(self) -> None:
        for disco in self.discos:
            if disco.disponivel():
                print(f'Disco {disco.id_disco}: idle')
            else:
                print(f'Disco {disco.id_disco}: Reservado para thread {disco.processo_atual.id_processo} no estado {disco.processo_atual.estado}')
        return