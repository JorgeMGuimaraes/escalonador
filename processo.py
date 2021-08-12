estados = {
    -1:  'não foi instanciado',
    0:   'novo',
    1:   'pronto',
    2:   'executando',
    3:   'suspenso',
    4:   'bloqueado',
    101: 'finalizado'
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
    
    def atualizar_andamento(self, andamento: bool) -> None:
        self.andamento.append(andamento)
        return

    def atualiza_estado(self, novo_estado: int) -> None:
        if self.estado == novo_estado: return

        print(f'Processo {self.id_processo} muda de estado: de {estados[self.estado]} para {estados[self.estado]}.')
        self.estado = novo_estado
        return
