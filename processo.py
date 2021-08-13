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
    def __init__(self, id_processo, chegada, prioridade, duracao, memoria, io) -> None:
        self.id_processo    = id_processo
        self.chegada        = chegada
        self.prioridade     = prioridade
        self.duracao        = duracao
        self.memoria        = memoria
        self.io             = io
        self.estado         = 0
        self.andamento      = []
    
    def executando(self, is_executando: bool) -> None:
        self.andamento.append(is_executando)
        if is_executando:
            self.duracao -= 1
            if self.duracao == 0:
                self.atualiza_estado(101)
        return
        
    def atualiza_estado(self, novo_estado: int) -> None:
        if self.estado == novo_estado: return

        self.estado = novo_estado
        return
