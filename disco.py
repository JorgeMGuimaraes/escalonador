class Disco:
    def __init__(self, id_disco) -> None:
        self.id_disco   = id_disco
        self.estado     = 0
        return
    
    def define_estado(self, novo_estado: int) -> None:
        self.estado = novo_estado
        return
