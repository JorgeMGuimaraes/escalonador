estado = {
    'nao_instanciado': -1,
    'novo': 0,
    'pronto': 1,
    'executando': 2,
    'suspenso': 3,
    'bloqueado': 4,
    'finalizado': 101
}
class Processo:
    def __init__(self, id_processo, chegada, prioridade, duracao, memoria, discos) -> None:
        self.id_processo    = id_processo
        self.chegada        = chegada
        self.prioridade     = prioridade
        self.duracao        = duracao
        self.memoria        = memoria
        self.discos         = discos
        self.estado         = estado['nao_instanciado']
        #self.quanta         = quanta
        self.andamento      = []
    
    def define_quantum(self, valor: int) -> None:
        self.quanta = valor
        return

    def executando(self) -> None:
        self.andamento.append(True)
        self.quanta     -= 1
        self.duracao    -= 1
        if self.terminou_de_processar():
            self.atualiza_estado(estado['finalizado'])
            return
        
        if self.is_tempo_real():
            return
        
        if self.usuario_sem_quantum():
            self.atualiza_estado(estado['pronto'])
            return

        if self.necessita_disco():
            self.atualiza_estado(estado['bloqueado'])
            return
        return

    def aguardando(self) -> None:
        self.andamento.append(False)
        return

    def atualiza_estado(self, novo_estado: int) -> None:
        if self.estado == novo_estado: return

        self.estado = novo_estado
        return

    def terminou_de_processar(self) -> bool:
        return self.duracao == 0

    def necessita_disco(self) -> bool:
        return self.discos > 0
    
    def is_tempo_real(self) -> bool:
        return self.prioridade == 0
    
    def usuario_sem_quantum(self) -> bool:
        return self.quanta == 0
