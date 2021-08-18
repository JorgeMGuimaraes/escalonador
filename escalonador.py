## imports
from processador import Processador
from processo import Processo, estado
from recursos import Recursos
from typing import List
from estado_processo import EstadoProcesso

# TODO: fix: memoria alocada
# TODO: fix: devolver memoria

class Escalonador:
    def __init__(self, recursos:Recursos, processos: List[Processo]) -> None:
        self.processos: List[Processo]                      = self.ordena_processos(processos)
        self.processos_nao_iniciados: List[Processo]        = []
        self.processos_novos: List[Processo]                = []
        self.processos_prontos: List[Processo]              = []
        self.processos_prontos_suspenso: List[Processo]     = []
        self.processos_executando: List[Processo]           = []
        # TODO: ver so pode renomear para prontosuspenso
        self.processos_suspensos: List[Processo]            = []
        self.processos_bloqueados: List[Processo]           = []
        self.processos_bloqueados_suspensos: List[Processo] = []
        self.processos_finalizados: List[Processo]          = []

        self.executar_operacao = {
            'Instanciar':                                   EstadoProcesso( atual=self.processos_nao_iniciados,
                                                                            proximo=self.processos_novos,
                                                                            estado=estado['novo'],
                                                                            msg_padrao='Novo processo instanciado em memória'),

            'Admitir como pronto-suspenso':                 EstadoProcesso( atual=self.processos_novos,
                                                                            proximo=self.processos_prontos_suspenso,
                                                                            estado=estado['pronto_suspenso'],
                                                                            msg_padrao='Foi admitido como pronto-suspenso'),

            'Admitir como pronto':                          EstadoProcesso( atual=self.processos_novos,
                                                                            proximo=self.processos_prontos,
                                                                            estado=estado['pronto'],
                                                                            msg_padrao='Foi admitido pronto'),

            'Ativar pronto-suspenso para pronto':           EstadoProcesso( atual=self.processos_prontos_suspenso,
                                                                            proximo=self.processos_prontos,
                                                                            estado=estado['pronto'],
                                                                            msg_padrao='Estava como pronto-suspenso e foi ativado. Está como pronto'),

            'Suspender pronto para pronto-suspenso':        EstadoProcesso( atual=self.processos_prontos,
                                                                            proximo=self.processos_prontos_suspenso,
                                                                            estado=estado['pronto_suspenso'],
                                                                            msg_padrao='Foi suspenso para o estado pronto-suspenso'),

            'Despachar pronto para executando':             EstadoProcesso( atual=self.processos_prontos,
                                                                            proximo=self.processos_executando,
                                                                            estado=estado['executando'],
                                                                            msg_padrao='Foi despachado para execução'),

            'Pausar executando para pronto':                EstadoProcesso( atual=self.processos_executando,
                                                                            proximo=self.processos_prontos,
                                                                            estado=estado['pronto'],
                                                                            msg_padrao='Estava executando e perdeu processador. Foi pausado e está no estado pronto'),

            'Bloqueia executando':                          EstadoProcesso( atual=self.processos_executando,
                                                                            proximo=self.processos_bloqueados,
                                                                            estado=estado['bloqueado'],
                                                                            msg_padrao='Estava escutando mas precisa ler/gravar. Foi bloqueado a espera de ocorrer evento'),

            'Evento ocorre, e vai para pronto':              EstadoProcesso( atual=self.processos_bloqueados,
                                                                            proximo=self.processos_prontos,
                                                                            estado=estado['pronto'],
                                                                            msg_padrao='Evento de leitura/escrita ocorreu e vai para pronto'),

            'Suspende bloqueado para bloqueado-suspenso':   EstadoProcesso( atual=self.processos_bloqueados,
                                                                            proximo=self.processos_bloqueados_suspensos,
                                                                            estado=estado['bloqueado_suspenso'],
                                                                            msg_padrao='Não há discos disponíveis, Suspende bloqueado para bloqueado-suspenso'),

            'Ativa suspenso-bloqueado para bloquado':       EstadoProcesso( atual=self.processos_bloqueados_suspensos,
                                                                            proximo=self.processos_bloqueados,
                                                                            estado=estado['bloqueado'],
                                                                            msg_padrao='Há discos disponíveis. Ativa suspenso-bloqueado para pronto-suspenso'),

            'Evento ocorre, e vai para pronto-suspenso':    EstadoProcesso( atual=self.processos_bloqueados_suspensos,
                                                                            proximo=self.processos_prontos_suspenso,
                                                                            estado=estado['pronto_suspenso'],
                                                                            msg_padrao='Evento ocorre, e vai para pronto-suspenso'),

            'Libera executando para finalizado':            EstadoProcesso( atual=self.processos_executando,
                                                                            proximo=self.processos_finalizados,
                                                                            estado=estado['finalizado'],
                                                                            msg_padrao='Processo terminou')

        }
        self.logs: List[str]                                = []

        for processo in self.processos:
            self.processos_nao_iniciados.append(processo)

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
        for processo in self.processos:
            if processo.estado < 100: return True

        return False
   
    def ativa_prontos_suspensos(self) -> None:
        for processo in self.processos_prontos_suspenso:
            if self.recursos.ha_memoria_disponivel():
                feedback_operacao = self.executar_operacao['Ativar pronto-suspenso para pronto'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
        return

    def reserva_discos(self) -> None:
        for processo in self.processos_bloqueados_suspensos:
            if self.recursos.ha_discos_disponiveis():
                for disco in self.recursos.discos:
                    if disco.pode_agregar(processo):
                        feedback_operacao = self.executar_operacao['Ativa suspenso-bloqueado para bloquado'].neste(processo)
                        self.adiciona_ao_log(feedback_operacao)

        for processo in self.processos_bloqueados:
            if self.recursos.ha_discos_disponiveis():
                for disco in self.recursos.discos:
                    disco.pode_agregar(processo)
            else:
                feedback_operacao = self.executar_operacao['Suspende bloqueado para bloqueado-suspenso'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
        return

    def executa_leitura_gravacao(self) -> None:
        for disco in self.recursos.discos:
            if not disco.gravar():
                continue

            processo                = disco.processo_atual
            disco.processo_atual    = None
            if processo.necessita_disco():
                feedback_operacao = self.executar_operacao['Suspende bloqueado para bloqueado-suspenso'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
                continue

            feedback_operacao = self.executar_operacao['Evento ocorre, e vai para pronto'].neste(processo)
            self.adiciona_ao_log(feedback_operacao)
        return

    def instanciar_processos(self, contador_quanta: int) -> None:
        for processo in self.processos_nao_iniciados:
            if processo.chegada == contador_quanta:
                feedback_operacao = self.executar_operacao['Instanciar'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
        return

    def admitir_processos(self) -> None:
        for processo in self.processos_novos:
            if self.recursos.ha_memoria_disponivel(processo):
                self.recursos.usa_memoria(processo.memoria)
                feedback_operacao = self.executar_operacao['Admitir como pronto'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
            else:
                feedback_operacao = self.executar_operacao['Admitir como pronto-suspenso'].neste(processo)
                self.adiciona_ao_log(feedback_operacao)
        return
    
    def despachar(self) -> None:
        for processo in self.processos_prontos:
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

        for processo in self.processos_executando:
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
        for processo in self.processos:
            if processo in self.processos_executando:
                continue
            if len(processo.andamento) <= quantum:
                processo.aguardando()
        return

    def adiciona_ao_log(self, feedback: str) -> None:
        self.logs.append(feedback)
        return

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
