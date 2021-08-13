## imports
from processador import Processador
from processo import Processo, estado
from recursos import Recursos
from typing import List

# TODO: fix: memoria alocada
# TODO: fix: devolver memoria

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
   
    def atribuir_politica(self, contador_quanta: int, quantum: int) -> None:
        #self.processa_fila_bloqueado()
        # self.processa_fila_suspenso()
        self.processa_fila_nao_iniciados(contador_quanta)        
        self.processa_fila_novos(quantum)
        self.processa_fila_prontos()
        self.processa_fila_executando()
        return
    
    # TODO: Sempre atualizar os estados dos processos
    def processa_fila_nao_iniciados(self, contador_quanta: int) -> None:
        for processo in self.processos_nao_iniciados:
            if processo.chegada == contador_quanta:
                self.processos_novos.append(processo)
                self.processos_nao_iniciados.remove(processo)
                self.logs.append(f'Processo {processo.id_processo}: é um novo processo')
        self.atualiza_andamento_idle(self.processos_nao_iniciados)
        return

    def processa_fila_novos(self, quantum: int) -> None:
        for processo in self.processos_novos:
            if self.recursos.ha_memoria_disponivel(processo.memoria):
                processo.define_quantum(quantum)
                self.recursos.usa_memoria(processo.memoria)
                # TODO: usa disco
                self.processos_prontos.append(processo)
                self.logs.append(f'Processo {processo.id_processo}: entrou na fila de prontos')
            else:
                self.processos_prontos_suspenso.append(processo)
                self.logs.append(f'Processo {processo.id_processo}: entrou na fila de prontos-suspensos')
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
                    self.logs.append(f'Processo {processo.id_processo}: será executado.')
                    break
        self.atualiza_andamento_idle(self.processos_prontos)
        return

    def processa_fila_executando(self) -> None:
        self.atualiza_andamento_idle(self.processos_finalizados)
        # processa
        for processador in self.recursos.processadores:
            if processador.processo_atual is not None:
                processador.executar()
                self.logs.append(f'Processo {processador.id_processador}: executando o Core {processador.processo_atual.id_processo}')

        for processo in self.processos_executando:
            #continua executando
            if processo.estado == estado['executando']:
                continue
            #vai para pronto
            elif processo.estado == estado['pronto']:
                self.processos_prontos.append(processo)
                self.processos_executando.remove(processo)
                self.logs.append(f'Processo {processo.id_processo} perdeu processador e foi encaminhado a lista de prontos.')
            #vai para bloqueado
            elif processo.estado == estado['bloqueado']:
                self.processos_bloqueados.append(processo)
                self.processos_executando.remove(processo)
                self.logs.append(f'Processo {processo.id_processo} precisa executar uma função IO e foi bloqueado.')
            #vai para terminado
            elif processo.estado == estado['finalizado']:
                self.processos_finalizados.append(processo)
                self.processos_executando.remove(processo)
                self.logs.append(f'Processo {processo.id_processo} terminou sua execução.')
                for processador in self.recursos.processadores:
                    if processador.processo_atual == processo:
                        processador.processo_atual = None
                    self.recursos.libera_memoria(processo.memoria)
        return

    def processa_fila_suspenso(self) -> None:
        self.atualiza_andamento_idle(self.processos_prontos_suspenso)
        return

    def processa_fila_bloqueado(self) -> None:
        self.atualiza_andamento_idle(self.processos_bloqueados)
        return

    def processa_fila_finalizado(self) -> None:
        self.atualiza_andamento_idle(self.processos_finalizados)
        return

    def atualiza_andamento_idle(self, processos: List[Processo]) -> None:
        for processo in processos:
            processo.aguardando()
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
