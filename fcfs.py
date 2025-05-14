import matplotlib.pyplot as plt

# FCFS - First-Come First-Served
def escalonar_fcfs(processos):
    processos.sort(key=lambda p: p['arrival'])  # ordena com base na hora de chegada
    tempo_atual = 0
    gantt = []  # armazena as informações de tempo de execução de cada processo

    print('FCFS - Escalonamento')
    print(f"{'Processo':<10}{'Início':<10}{'Fim':<10}{'Espera':<10}{'Turnaround'}")

    for processo in processos:
        inicio = max(tempo_atual, processo['arrival'])
        fim = inicio + processo['burst']
        espera = inicio - processo['arrival']
        turnaround = fim - processo['arrival']

        gantt.append((processo['id'], inicio, fim))
        tempo_atual = fim

        print(f"{processo['id']:<10}{inicio:<10}{fim:<10}{espera:<10}{turnaround}")

    desenhar_gantt(gantt)

def desenhar_gantt(gantt):
    fig, gnt = plt.subplots()
    gnt.set_title("Gráfico de Gantt - FCFS")
    gnt.set_xlabel("Tempo")
    gnt.set_ylabel("Processos")

    gnt.set_yticks([15 + i*10 for i in range(len(gantt))])
    gnt.set_yticklabels([processo[0] for processo in gantt])
    gnt.set_ylim(0, 10 + len(gantt)*20)

    for i, (pid, inicio, fim) in enumerate(gantt):
        gnt.broken_barh([(inicio, fim - inicio)], (10 + i*10, 9), facecolors=('tab:blue'))

    plt.show()
