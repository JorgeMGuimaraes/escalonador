## imports
from processador import Processador
from processo import Processo, estado
from recursos import Recursos
from typing import List
from estado_processo import EstadoProcesso

# TODO: fix: memoria alocada
# TODO: fix: devolver memoria

class Escalonador:
    def __init__(self, recursos:Recursos, threads: List[Processo]) -> None:
        self.threads: List[Processo]                      = self.ordena_processos(threads)
        self.lista_nao_iniciados: List[Processo]        = []
        self.lista_novos: List[Processo]                = []
        self.lista_prontos: List[Processo]              = []
        self.lista_prontos_suspenso: List[Processo]     = []
        self.lista_executando: List[Processo]           = []
        self.lista_bloqueados: List[Processo]           = []
        self.lista_bloqueados_suspensos: List[Processo] = []
        self.lista_finalizados: List[Processo]          = []

        self.executar_operacao = {
            'Instanciar':                                   EstadoProcesso( atual=self.lista_nao_iniciados,
                                                                            proximo=self.lista_novos,
                                                                            estado=estado['novo'],
                                                                            msg_padrao='Novo processo instanciado em memória'),

            'Admitir como pronto-suspenso':                 EstadoProcesso( atual=self.lista_novos,
                                                                            proximo=self.lista_prontos_suspenso,
                                                                            estado=estado['pronto_suspenso'],
                                                                            msg_padrao='Foi admitido como pronto-suspenso'),

            'Admitir como pronto':                          EstadoProcesso( atual=self.lista_novos,
                                                                            proximo=self.lista_prontos,
                                                                            estado=estado['pronto'],
                                                                            msg_padrao='Foi admitido pronto'),

            'Ativar pronto-suspenso para pronto':           EstadoProcesso( atual=self.lista_prontos_suspenso,
                                                                            proximo=self.lista_prontos,
                                                                            estado=estado['pronto'],
                                                                            msg_padrao='Estava como pronto-suspenso e foi ativado. Está como pronto'),

            'Suspender pronto para pronto-suspenso':        EstadoProcesso( atual=self.lista_prontos,
                                                                            proximo=self.lista_prontos_suspenso,
                                                                            estado=estado['pronto_suspenso'],
                                                                            msg_padrao='Foi suspenso para o estado pronto-suspenso'),

            'Despachar pronto para executando':             EstadoProcesso( atual=self.lista_prontos,
                                                                            proximo=self.lista_executando,
                                                                            estado=estado['executando'],
                                                                            msg_padrao='Foi despachado para execução'),

            'Pausar executando para pronto':                EstadoProcesso( atual=self.lista_executando,
                                                                            proximo=self.lista_prontos,
                                                                            estado=estado['pronto'],
                                                                            msg_padrao='Estava executando e perdeu processador. Foi pausado e está no estado pronto'),

            'Bloqueia executando':                          EstadoProcesso( atual=self.lista_executando,
                                                                            proximo=self.lista_bloqueados,
                                                                            estado=estado['bloqueado'],
                                                                            msg_padrao='Estava executando mas precisa ler/gravar. Foi bloqueado a espera de ocorrer evento'),

            'Evento ocorre, e vai para pronto':              EstadoProcesso( atual=self.lista_bloqueados,
                                                                            proximo=self.lista_prontos,
                                                                            estado=estado['pronto'],
                                                                            msg_padrao='Evento de leitura/escrita ocorreu e vai para pronto'),

            'Suspende bloqueado para bloqueado-suspenso':   EstadoProcesso( atual=self.lista_bloqueados,
                                                                            proximo=self.lista_bloqueados_suspensos,
                                                                            estado=estado['bloqueado_suspenso'],
                                                                            msg_padrao='Não há discos disponíveis, Suspende bloqueado para bloqueado-suspenso'),

            'Ativa suspenso-bloqueado para bloquado':       EstadoProcesso( atual=self.lista_bloqueados_suspensos,
                                                                            proximo=self.lista_bloqueados,
                                                                            estado=estado['bloqueado'],
                                                                            msg_padrao='Há discos disponíveis. Ativa suspenso-bloqueado para pronto-suspenso'),

            'Evento ocorre, e vai para pronto-suspenso':    EstadoProcesso( atual=self.lista_bloqueados_suspensos,
                                                                            proximo=self.lista_prontos_suspenso,
                                                                            estado=estado['pronto_suspenso'],
                                                                            msg_padrao='Evento ocorre, e vai para pronto-suspenso'),

            'Libera executando para finalizado':            EstadoProcesso( atual=self.lista_executando,
                                                                            proximo=self.lista_finalizados,
                                                                            estado=estado['finalizado'],
                                                                            msg_padrao='Processo terminou')

        }
        self.logs: List[str]                                = []

        for processo in self.threads:
            self.lista_nao_iniciados.append(processo)

        self.recursos                                       = recursos
        # TODO: remover mgs desnecessarias
        self.mensagens                                      = {
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
        for thread in self.threads:
            if thread.estado < 100: return True

        return False
   
    def ativa_prontos_suspensos(self) -> None:
        for processo in self.lista_prontos_suspenso:
            if self.recursos.ha_memoria_disponivel():
                feedback_operacao = self.executar_operacao['Ativar pronto-suspenso para pronto'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
        return

    def reserva_discos(self) -> None:
        for processo in self.lista_bloqueados_suspensos:
            if self.recursos.ha_discos_disponiveis():
                for disco in self.recursos.discos:
                    if disco.pode_agregar(processo):
                        feedback_operacao = self.executar_operacao['Ativa suspenso-bloqueado para bloquado'].neste(processo)
                        self.adiciona_ao_log(feedback_operacao)

        for processo in self.lista_bloqueados:
            if self.recursos.ha_discos_disponiveis():
                for disco in self.recursos.discos:
                    disco.pode_agregar(processo)
            else:
                feedback_operacao = self.executar_operacao['Suspende bloqueado para bloqueado-suspenso'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
        return

    def executa_leitura_gravacao(self) -> None:
        threads_gravaram = []
        for disco in self.recursos.discos:
            if not disco.gravar():
                continue

            processo                = disco.processo_atual
            disco.processo_atual    = None
            if processo not in threads_gravaram:
                threads_gravaram.append(processo)

            if processo.necessita_disco():
                feedback_operacao = self.executar_operacao['Suspende bloqueado para bloqueado-suspenso'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
                continue
        
        for thread in threads_gravaram:
            feedback_operacao = self.executar_operacao['Evento ocorre, e vai para pronto'].neste(thread)
            self.adiciona_ao_log(feedback_operacao)
        return

    def instanciar_processos(self, contador_quanta: int) -> None:
        for processo in self.lista_nao_iniciados:
            if processo.chegada == contador_quanta:
                feedback_operacao = self.executar_operacao['Instanciar'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
        return

    def admitir_processos(self) -> None:
        for processo in self.lista_novos:
            if self.recursos.ha_memoria_disponivel(processo):
                self.recursos.usa_memoria(processo.memoria)
                feedback_operacao = self.executar_operacao['Admitir como pronto'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
            else:
                feedback_operacao = self.executar_operacao['Admitir como pronto-suspenso'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
        return
    
    def despachar(self) -> None:
        for processo in self.lista_prontos:
            for processador in self.recursos.processadores:
                if processador.pode_agregar(processo):
                    feedback_operacao = self.executar_operacao['Despachar pronto para executando'].neste(processo)
                    self.adiciona_ao_log(feedback_operacao)
                    break

        return

    def processar_threads(self) -> None:
        # processa
        for processador in self.recursos.processadores:
            if processador.pode_executar():
                self.logs.append(f'Processo {processador.processo_atual.id_processo}: Executou no Core {processador.id_processador}')

        for processo in self.lista_executando:
            #continua executando
            if processo.estado == estado['executando']:
                continue
            #vai para pronto
            elif processo.estado == estado['pronto']:
                feedback_operacao = self.executar_operacao['Pausar executando para pronto'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
                for processador in self.recursos.processadores:
                    processador.liberar(processo)
            #vai para bloqueado
            elif processo.estado == estado['bloqueado']:
                feedback_operacao = self.executar_operacao['Bloqueia executando'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
                for processador in self.recursos.processadores:
                    processador.liberar(processo)
            #vai para terminado
            elif processo.estado == estado['finalizado']:
                feedback_operacao = self.executar_operacao['Libera executando para finalizado'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
                for processador in self.recursos.processadores:
                    processador.liberar(processo)
                    self.recursos.libera_memoria(processo.memoria)
        return

    def atualiza_estado_idle(self, quantum: int) -> None:
        for thread in self.threads:
            if thread in self.lista_executando:
                continue
            if len(thread.andamento) <= quantum:
                thread.aguardando()
        return

    def adiciona_ao_log(self, feedback: str) -> None:
        self.logs.append(feedback)
        return

    ## exibe
    def imprime_processos_recebidos(self) -> None:
        for thread in self.threads:
            tempo = 'tempo real' if thread.prioridade == 0 else 'usuário'
            discos = 'sem necessidade de recursos de E/S' if thread.discos == 0 else f'requer { thread.discos} unidade(s) de disco(s)'
            print(f'Processo {thread.id_processo}: chegada no momento {thread.chegada}, prioridade {thread.prioridade} ({tempo}), duração de {thread.duracao} segundos de CPU e memória de {thread.memoria} MBytes, {discos} disco(s)')
        return

    def imprime_andamento(self, quanta:int) -> None:
        espacamento = '    '
        s = 'Andamento:\n'
        s+= '                 |'
        for quantum in range(quanta + 1):
            s += f'{quantum:>2}|'
        print(f'{s}\n')

        for thread in self.threads:
            s = f'{espacamento}Processo {thread.id_processo:>2}: |'
            for processou in thread.andamento:
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
