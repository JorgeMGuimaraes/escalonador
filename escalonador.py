#!/usr/bin/python3
## imports
from processo   import Processo
from recursos   import Recursos
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

def ordena_processos(processos:  List[Processo]) -> List[Processo]:
    return sorted(processos, key = lambda proc: (proc.chegada, proc.prioridade))

def imprime_processos_recebidos(processos:  List[Processo]) -> None:
    for processo in processos:
        tempo = 'tempo real' if processo.prioridade == 0 else 'usuário'
        disco = 'sem necessidade de recursos de E/S' if processo.io == 0 else f'requer { processo.io} unidade de disco'
        print(f'Processo {processo.id_processo}: chegada no momento {processo.chegada}, prioridade {processo.prioridade} ({tempo}), duração de {processo.duracao} segundos de CPU e memória de {processo.memoria} MBytes, {disco}')
    return

def imprime_andamento(quantum: int, recursos: Recursos) -> None:
    espacamento = '    '
    s  = 'Estado Atual:\n'
    s += 'Recursos disponíveis:\n'
    s += f'{espacamento}CPU:     {recursos.cpus}\n'
    s += f'{espacamento}Discos:  {recursos.discos}\n'
    s += f'{espacamento}MP:      {recursos.memoria}MB\n'
    s += f'{espacamento}Quantum: {quantum}\n'
    print(s)
    return

def main():
    processos   = ordena_processos(processa_entrada())
    recursos    = Recursos()
    quantum     = 0

    imprime_andamento(quantum, recursos)
    imprime_processos_recebidos(processos)
    return

## Programa principal
if __name__ == "__main__": main()

"""
Estado Atual:
Recursos disponíveis:
    CPU:    4
    Discos: 4
    MP:     15246 MB
    Quantum: 12
Processos:
    Novo:        Processo 0
    Novo:        Processo 1
    Processando: Processo 1
Andamento:
                |12|13|14|15|
    Processo 0: |* | 
    Processo 1: |  |

"""
