#!/usr/bin/python3
## imports
from processo       import Processo
from recursos       import Recursos

from typing     import List
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

def ordena_processos(processos: List[Processo]) -> List[Processo]:
    return sorted(processos, key = lambda proc: (proc.chegada, proc.prioridade))

def imprime_processos_recebidos(processos:  List[Processo]) -> None:
    for processo in processos:
        tempo = 'tempo real' if processo.prioridade == 0 else 'usuário'
        disco = 'sem necessidade de recursos de E/S' if processo.io == 0 else f'requer { processo.io} unidade de disco'
        print(f'Processo {processo.id_processo}: chegada no momento {processo.chegada}, prioridade {processo.prioridade} ({tempo}), duração de {processo.duracao} segundos de CPU e memória de {processo.memoria} MBytes, {disco}')
    print()
    return

def imprime_recursos(quantum: int, recursos: Recursos) -> None:
    espacamento = '    '
    s  = 'Estado Atual:\n'
    s += f'Quantum: {quantum}\n'
    s += 'Recursos:\n'
    print(s)
    return

def imprime_andamento(quanta:int, processos: List[Processo]) -> None:
    espacamento = '    '
    s = 'Andamento:\n'
    s+= '                 |'
    for quantum in range(quanta + 1):
        s += f'{quantum:>2}|'
    print(f'{s}\n')

    for processo in processos:
        s = f'{espacamento}Processo {processo.id_processo:>2}: |'
        for processou in processo.andamento:
            s += '* |' if processou else '  |'
        print(f'{s}\n')
    return

def continuar_processando(processos: List[Processo]) -> bool:
    for processo in processos:
        if processo.estado < 100: return True

    return False

def main():
    cpus            = 4
    discos          = 4
    memoria         = 16 * 1024
    recursos        = Recursos(cpus, discos, memoria)
    processos       = ordena_processos(processa_entrada())
    quanta          = 0
    imprime_processos_recebidos(processos)
    while continuar_processando(processos):
        imprime_recursos(quanta, recursos)
        recursos.imprime_processadores()
        recursos.imprime_memoria()
        recursos.imprime_discos()
        imprime_andamento(quanta, processos)
        quanta += 1
        _       = input()
    return

## Programa principal
if __name__ == "__main__": main()
