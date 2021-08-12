status = {
    0: 'ainda não foi instanciado',
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
        self.status         = 0
