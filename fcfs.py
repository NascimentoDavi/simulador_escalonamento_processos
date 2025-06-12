import matplotlib.pyplot as plt

# Implementação do algoritmo First-Come - First Served - Um dos algoritmos mais simples utilizados em sistemas operacionas para gerenciar a ordem da execução de processos

# FCFS - First-Come First-Served
def escalonar_fcfs(processos):
    processos.sort(key=lambda p: p['arrival'])  # ordena com base na hora de chegada
    tempo_atual = 0
    gantt = []  # armazena as informações de tempo de execução de cada processo

    print('FCFS - Escalonamento')

    # < : alinhamento a esquerda
    # 10: ocupar 10 caracteres
    print(f"{'Processo':<10}{'Início':<10}{'Fim':<10}{'Espera':<10}{'Turnaround'}")

    for processo in processos:

        # Processo só tem início quando o processador está livre (tempo_atual) e quando o próximo processo chega (processo['arrival']). Max() aciona o valor máximo, maior, para garantir que comece apenas qundo o processador está livre.
        inicio = max(tempo_atual, processo['arrival']) 
        
        fim = inicio + processo['burst'] # Burst é o tempo de execução necessário, ou seja, o "tempo de CPU".

        espera = inicio - processo['arrival']

        turnaround = fim - processo['arrival'] # Tempo total que processo leva, desde que chegou até terminar sua execução

        gantt.append((processo['id'], inicio, fim))
        
        tempo_atual = fim

        # < : alinhamento à esquerda
        # 10: ocupa 10 caracteres
        print(f"{processo['id']:<10}{inicio:<10}{fim:<10}{espera:<10}{turnaround}")

    desenhar_gantt(gantt)

def desenhar_gantt(gantt):
    import matplotlib.colors as mcolors

    fig, gnt = plt.subplots()
    gnt.set_title("Gráfico de Gantt - FCFS")
    gnt.set_xlabel("Tempo")
    gnt.set_ylabel("Processos")

    gnt.set_yticks([15 + i*10 for i in range(len(gantt))])
    gnt.set_yticklabels([processo[0] for processo in gantt])
    gnt.set_ylim(0, 10 + len(gantt)*20)

    cores = list(mcolors.TABLEAU_COLORS.values())

    for i, (pid, inicio, fim) in enumerate(gantt):
        cor = cores[i % len(cores)]
        gnt.broken_barh([(inicio, fim - inicio)], (10 + i*10, 9), facecolors=(cor))

    plt.show()