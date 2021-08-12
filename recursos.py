class Recursos:
    """O sistema possui os seguintes recursos:
        * quatro CPUs
        * quatro discos
        * 16GB de memória principal
    """
    def __init__(self) -> None:
        self.cpus       = 4
        self.discos     = 4
        self.memoria    = 1024*16

    def usar_cpu(self) -> bool:
        if self.cpus == 0: return False
    
        self.cpus -= 1
        return True

    def liberar_cpu(self) -> None:
        self.cpus += 1
        return

    def usar_disco(self) -> bool:
        if self.discos == 0: return False
    
        self.discos -= 1
        return True

    def liberar_disco(self) -> None:
        self.discos += 1
        return

    def usar_memoria(self, valor_consumido) -> bool:
        if self.memoria - valor_consumido < 0: return False
    
        self.memoria -= valor_consumido
        return True
    def liberar_memeoria(self, valor_liberado) -> None:
        self.memeoria += valor_liberado
        return
