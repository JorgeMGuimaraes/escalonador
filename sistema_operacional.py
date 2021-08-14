#!/usr/bin/python3
## imports
import io
from escalonador    import Escalonador
from processo       import Processo
from recursos       import Recursos
from typing         import List
## classes

## definicoes
def processa_entrada(quantum: int) -> List[Processo]:
    filename            ='entrada'
    contador_processos  = 0
    processos           = []
    with open(file=filename,mode='r') as arquivo:
        for linha in arquivo:
            if linha.startswith('#') or linha == '\n' or linha == '':
                continue
            valores     = linha.split(',')
            chegada     = int(valores[0].strip())
            prioridade  = int(valores[1].strip())
            duracao     = int(valores[2].strip())
            memoria     = int(valores[3].strip())
            discos      = int(valores[4].strip())
            entrada     = Processo(
                                    id_processo = contador_processos,
                                    chegada     = chegada,
                                    prioridade  = prioridade,
                                    duracao     = duracao,
                                    memoria     = memoria,
                                    discos      = discos                                 )
            entrada.define_quantum(quantum)
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
    # TODO: pegar valores do usuário
    quantum         = 2
    contador_quanta = 0
    cpus            = 4
    discos          = 4
    memoria         = 16 * 1024
    recursos        = Recursos(cpus, discos, memoria)
    escalonador     = Escalonador(recursos, processa_entrada(quantum))
    escalonador.imprime_processos_recebidos()
    print()
    while escalonador.continuar_processando():
        imprime_header(contador_quanta)
        escalonador.atribuir_politica(contador_quanta, quantum)
        recursos.imprime_processadores()
        recursos.imprime_memoria()
        recursos.imprime_discos()
        escalonador.imprime_log_processos()
        escalonador.imprime_andamento(contador_quanta)
        contador_quanta += 1
        _               = input()
    return

## Programa principal
if __name__ == "__main__": main()
