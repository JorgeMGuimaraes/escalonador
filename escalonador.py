#!/usr/bin/python3
## imports
from recursos   import Recursos
from typing     import List
## classes

class Processo:
    def __init__(self, id_processo, chegada, prioridade, duracao, memoria, io) -> None:
        self.id_processo    = id_processo
        self.chegada        = chegada
        self.prioridade     = prioridade
        self.duracao        = duracao
        self.memoria        = memoria
        self.io             = io

## definicoes
def processa_entrada() -> List[Processo]:
    filename            ='entrada'
    contador_processos  = 0
    processos           = []
    with open(file=filename,mode='r') as arquivo:
        for linha in arquivo:
            valores = linha.split(', ')
            entrada = Processo(contador_processos, int(valores[0].strip()), int(valores[1].strip()), int(valores[2].strip()), int(valores[3].strip()), int(valores[4].strip()))
            processos.append(entrada)
            contador_processos += 1
    return processos

def ordena_processos(processos:  List[Processo]) -> List[Processo]:
    return sorted(processos, key = lambda proc: (proc.chegada, proc.prioridade))

def imprime_processos_recebidos(processos:  List[Processo]) -> None:
    for processo in processos:
        tempo = 'tempo real' if processo.prioridade == 0 else 'usuário'
        disco = 'sem necessidade de recursos de E/S' if processo.io == 0 else f'requer { processo.io} unidade de disco'
        print(f'Processo {processo.id_processo}: chegada no momento {processo.chegada}, prioridade {processo.prioridade} ({tempo}), duração de {processo.duracao} segundos de CPU e memória de {processo.memoria} MBytes, {disco}')

#sorted(s, key = lambda x: (x[1], x[2]))
def main():
    processos = ordena_processos(processa_entrada())
    imprime_processos_recebidos(processos)
    r = Recursos()
    print(r.cpus)

## Programa principal
if __name__ == "__main__": main()

