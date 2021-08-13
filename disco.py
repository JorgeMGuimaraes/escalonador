estado_disco = {
    'idle': 0,
    'ocupado': 1
}

class Disco:
    def __init__(self, id_disco) -> None:
        self.id_disco   = id_disco
        self.estado     = estado_disco['idle']
        return
    
    def define_estado(self, novo_estado: int) -> None:
        self.estado = novo_estado
        return

    def disponivel(self) -> bool:
        return self.estado == estado_disco['idle']