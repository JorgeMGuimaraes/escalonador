#!/usr/bin/python3
## imports
from escalonador    import Escalonador
from processo       import Processo
from recursos       import Recursos
from typing         import List
## classes

## definicoes
def processa_entrada() -> List[Processo]:
    filename            ='entrada'
    contador_processos  = 0
    processos           = []
    with open(file=filename,mode='r') as arquivo:
        for linha in arquivo:
            valores             = linha.split(', ')
            entrada             = Processo(contador_processos, int(valores[0].strip()), int(valores[1].strip()), int(valores[2].strip()), int(valores[3].strip()), int(valores[4].strip()))
            processos.append(entrada)
            contador_processos  += 1
    return processos

def imprime_header(quantum: int) -> None:
    espacamento = '    '
    s  = 'Estado Atual:\n'
    s += f'Quantum: {quantum}\n'
    print(s)
    return

def main():
    cpus            = 4
    discos          = 4
    memoria         = 16 * 1024
    recursos        = Recursos(cpus, discos, memoria)
    escalonador     = Escalonador(recursos, processa_entrada())
    quanta          = 0
    escalonador.imprime_processos_recebidos()
    print()
    while escalonador.continuar_processando():
        imprime_header(quanta)
        recursos.imprime_processadores()
        recursos.imprime_memoria()
        recursos.imprime_discos()
        escalonador.imprime_andamento(quanta)
        quanta += 1
        _       = input()
    return

## Programa principal
if __name__ == "__main__": main()
