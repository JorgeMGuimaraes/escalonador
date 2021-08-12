#!/usr/bin/python3

## classes
class Entrada:
    def __init__(self, processo, chegada, prioridade, duracao, memoria, io) -> None:
        self.processo   = processo
        self.chegada    = chegada
        self.prioridade = prioridade
        self.duracao    = duracao
        self.memoria    = memoria
        self.io         = io

## definicoes
def processa_entrada():
    filename='entrada'
    contador_processos = 0
    entradas = []
    with open(file=filename,mode='r') as arquivo:
        for linha in arquivo:
            valores = linha.split(', ')
            entrada = Entrada(contador_processos, int(valores[0].strip()), int(valores[1].strip()), int(valores[2].strip()), int(valores[3].strip()), int(valores[4].strip()))
            tempo = 'tempo real' if entrada.prioridade == 0 else 'usuário'
            disco = 'sem necessidade de recursos de E/S' if entrada.io == 0 else f'requer { entrada.io} unidade de disco'
            print(f'Processo {entrada.processo}: chegada no momento {entrada.chegada}, prioridade {entrada.prioridade} ({tempo}), duração de {entrada.duracao} segundos de CPU e memória de {entrada.memoria} MBytes, {disco}')
            entradas.append(entrada)
            contador_processos += 1
    return

def main():
    processa_entrada()

## Programa principal
if __name__ == "__main__": main()

