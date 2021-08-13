## imports
from processador import Processador
from processo import Processo
from recursos import Recursos
from typing import List


class Escalonador:
    def __init__(self, recursos:Recursos, processos: List[Processo]) -> None:
        self.processos: List[Processo]                  = self.ordena_processos(processos)
        self.processos_nao_iniciados: List[Processo]    = []
        self.processos_novos: List[Processo]            = []
        self.processos_prontos: List[Processo]          = []
        self.processos_prontos_suspenso: List[Processo] = []
        self.processos_executando: List[Processo]       = []
        self.processos_suspensos: List[Processo]        = []
        self.processos_bloqueados: List[Processo]       = []
        self.processos_finalizados: List[Processo]      = []

        self.logs: List[str]                            = []

        for processo in self.processos:
            self.processos_nao_iniciados.append(processo)

        self.recursos   = recursos
        return
    
    ## carrega
    def ordena_processos(self, processos: List[Processo]) -> List[Processo]:
        return sorted(processos, key = lambda proc: (proc.chegada, proc.prioridade))

    ## usa
    def continuar_processando(self) -> bool:
        for processo in self.processos:
            if processo.estado < 100: return True

        return False

    def politica_fifo(self, processador: Processador) -> None:
        # se terminou remover de executando, remover de executando
        processador.processo_atual.executando(True)

        processador.processo_atual.estado = 2
        processador.processo_atual.duracao -= 1
        return

    def politica_feedback(self) -> None:
        # se quantum passou, remover de executando
        return
    
    def atribuir_politica(self, quantum: int) -> None:
        #self.processa_fila_executando()
        #self.processa_fila_bloqueado()
        # self.processa_fila_suspenso()
        self.processar_fila_nao_iniciados(quantum)        
        self.processa_fila_novos()
        self.processa_fila_prontos()
        return
    
    def processar_fila_nao_iniciados(self, quantum: int) -> None:
        for processo in self.processos_nao_iniciados:
            if processo.chegada == quantum:
                self.processos_novos.append(processo)
                self.processos_nao_iniciados.remove(processo)
                self.logs.append(f'Processo {processo.id_processo} é um novo processo')
        return

    def processa_fila_novos(self) -> None:
        for processo in self.processos_novos:
            if self.recursos.ha_memoria_disponivel(processo.memoria):
                self.recursos.usa_memoria(processo.memoria)
                self.processos_prontos.append(processo)
                self.logs.append(f'Processo {processo.id_processo} entrou na fila de prontos')
            else:
                self.processos_prontos_suspenso.append(processo)
                self.logs.append(f'Processo {processo.id_processo} entrou na fila de prontos-suspensos')
            self.processos_novos.remove(processo)
        return

    def processa_fila_prontos(self) -> None:
        for processo in self.processos_prontos:
            for processador in self.recursos.processadores:
                if processador.processo_atual is None:
                    processador.processo_atual  = processo
                    processo.estado             = 2
                    self.processos_executando.append(processo)
                    self.processos_prontos.remove(processo)
                    self.logs.append(f'Processo {processo.id_processo} será executado.')
                    break
        return

    def processa_fila_executando(self) -> None:
        tempo_real  = 0
        usuario     = 1

        for processo in self.processos_executando:
            if processo.estado == 1: # pronto
                for processador in self.recursos.processadores:
                    if processador.processo_atual is None:
                        processador.processo_atual = processo
                pass
            elif processo.estado == 2: # executando
                #checa se ainda pode executar
                    #se nao pode: atualiza estado, mode de fila
                pass



        # atribui processador
        for processador in self.recursos.processadores:
            if processador.processo_atual is None:
                pass
            else:
                pass
            for processo in self.processos_executando:
                if processo.estado == 1:
                    processo.estado = 2
                    processador.processo_atual = processo
        # processa
        for processador in self.recursos.processadores:
            prioridade  = processador.processo_atual.prioridade
            if prioridade == usuario:
                processador.executar(self.politica_feedback)
                continue

            processador.executar(self.politica_fifo)
        return

    def processa_fila_suspenso(self) -> None:
        return

    def processa_fila_bloqueado(self) -> None:
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
    
    def imprime_log_processos(self) -> None:
        print(f'\nLog de Processos:')
        for log in self.logs:
            print(log)
        print()
        self.logs.clear()
        return
