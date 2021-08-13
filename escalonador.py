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
        # TODO: ver so pode renomear para prontosuspenso
        self.processos_suspensos: List[Processo]        = []
        self.processos_bloqueados: List[Processo]       = []
        self.processos_bloqueados_suspensos: List[Processo]  = []
        self.processos_finalizados: List[Processo]      = []

        self.logs: List[str]                            = []

        for processo in self.processos:
            self.processos_nao_iniciados.append(processo)

        self.recursos   = recursos

        self.mensagens = {
            'novo': 'Novo processo instanciado em memória',
            'novo_pronto': 'Entrou na fila de prontos.',
            'pronto_suspenso': 'Entrou na fila de prontos-suspensos.',
            'perdeu_processador': 'Perdeu processador e foi encaminhado a lista de prontos.',
            'sera_executado': 'Será executado.',
            'foi_bloqueado': 'Precisa executar uma função IO e foi bloqueado.',
            'bloqueado_suspenso': 'Reservou ao menos uma unidade de disco e entrou na fila de bloqueados-suspensos',
            'terminou': 'Terminou sua execução.',
            'pronto_bloqueado': 'Termonou de leitura/escrita e entrou na fila de prontos-bloqueados'
        }
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
        self.processa_fila_bloqueado()
        self.processa_fila_suspenso()
        self.processa_fila_nao_iniciados(contador_quanta)        
        self.processa_fila_novos(quantum)
        self.processa_fila_prontos()
        self.processa_fila_executando()
        return
    
    # TODO: Sempre atualizar os estados dos processos
    def processa_fila_nao_iniciados(self, contador_quanta: int) -> None:
        for processo in self.processos_nao_iniciados:
            if processo.chegada == contador_quanta:
                self.atualiza_estado(processo, self.processos_nao_iniciados, self.processos_novos, 'novo')
        self.atualiza_andamento_idle(self.processos_nao_iniciados)
        return

    def processa_fila_novos(self, quantum: int) -> None:
        for processo in self.processos_novos:
            if self.recursos.ha_memoria_disponivel(processo):
                processo.define_quantum(quantum)
                self.recursos.usa_memoria(processo.memoria)
                self.atualiza_estado(processo, self.processos_novos, self.processos_prontos, 'novo_pronto')

            else:
                self.atualiza_estado(processo, self.processos_novos, self.processos_prontos_suspenso, 'pronto_suspenso')
        return

    def processa_fila_prontos(self) -> None:
        for processo in self.processos_prontos:
            for processador in self.recursos.processadores:
                if processador.pode_agregar(processo):
                    self.atualiza_estado(processo, self.processos_prontos, self.processos_executando, 'sera_executado')
                    break

        self.atualiza_andamento_idle(self.processos_prontos)
        return

    def processa_fila_executando(self) -> None:
        self.atualiza_andamento_idle(self.processos_finalizados)
        # processa
        for processador in self.recursos.processadores:
            if processador.pode_executar():
                self.logs.append(f'Processo {processador.processo_atual.id_processo}: Executou no Core {processador.id_processador}')

        for processo in self.processos_executando:
            #continua executando
            if processo.estado == estado['executando']:
                continue
            #vai para pronto
            elif processo.estado == estado['pronto']:
                self.atualiza_estado(processo, self.processos_executando, self.processos_prontos, 'perdeu_processador')
                for processador in self.recursos.processadores:
                    processador.liberar(processo)
            #vai para bloqueado
            elif processo.estado == estado['bloqueado']:
                self.atualiza_estado(processo, self.processos_executando, self.processos_bloqueados, 'foi_bloqueado', novo_estado='bloqueado')
                for processador in self.recursos.processadores:
                    processador.liberar(processo)
            #vai para terminado
            elif processo.estado == estado['finalizado']:
                self.atualiza_estado(processo, self.processos_executando, self.processos_finalizados, 'terminou')
                for processador in self.recursos.processadores:
                    processador.liberar(processo)
                    self.recursos.libera_memoria(processo.memoria)
        return

    def processa_fila_suspenso(self) -> None:
        self.atualiza_andamento_idle(self.processos_prontos_suspenso)
        return

    def processa_fila_bloqueado(self) -> None:
        for processo in self.processos_bloqueados:
            if self.recursos.ha_discos_disponiveis():
                for disco in self.recursos.discos:
                    if disco.pode_agregar(processo):
                        self.atualiza_estado(processo, self.processos_bloqueados, self.processos_bloqueados_suspensos, 'bloqueado_suspenso', novo_estado='bloqueado_suspenso')
                        self.logs.append(f'Processo {processo.id_processo}: Reservou o disco {disco.id_disco}')
    
        self.atualiza_andamento_idle(self.processos_bloqueados)
        return

    def processa_bloqueado_suspenso(self) -> None:
        self.atualiza_andamento_idle(self.processos_bloqueados_suspensos)
        for disco in self.recursos.discos:
            if disco.gravar():
                self.logs.append(f'Processo {disco.processo_atual.id_processo}: Está lendo/gravando no disco {disco.id_disco}')

        for processo in self.processos_bloqueados_suspensos:
            self.atualiza_estado(processo, self.processos_bloqueados_suspensos, self.processos_prontos_suspenso, 'pronto_bloqueado', 'pronto_suspenso')
        return

    def processa_fila_finalizado(self) -> None:
        self.atualiza_andamento_idle(self.processos_finalizados)
        return

    def atualiza_andamento_idle(self, processos: List[Processo]) -> None:
        for processo in processos:
            processo.aguardando()
        return
    
    def atualiza_estado(self, processo: Processo, lista_atual: List[Processo], lista_nova: List[Processo], msg: str, novo_estado: str=None):
        lista_nova.append(processo)
        lista_atual.remove(processo)
        if novo_estado:
            processo.estado = estado[novo_estado]
        self.logs.append(f'Processo {processo.id_processo}: {self.mensagens[msg]}')
        # TODO: pass?
        pass
    ## exibe
    def imprime_processos_recebidos(self) -> None:
        for processo in self.processos:
            tempo = 'tempo real' if processo.prioridade == 0 else 'usuário'
            discos = 'sem necessidade de recursos de E/S' if processo.discos == 0 else f'requer { processo.discos} unidade(s) de disco(s)'
            print(f'Processo {processo.id_processo}: chegada no momento {processo.chegada}, prioridade {processo.prioridade} ({tempo}), duração de {processo.duracao} segundos de CPU e memória de {processo.memoria} MBytes, {discos} disco(s)')
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
