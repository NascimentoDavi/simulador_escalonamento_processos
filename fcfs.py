import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

# FCFS - First-Come First-Served
def escalonar_fcfs(processos, nome_arquivo="fcfs"):
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

    desenhar_gantt(gantt, nome_arquivo)

def desenhar_gantt(gantt, nome_arquivo="fcfs"):
    os.makedirs("graficos", exist_ok=True)

    fig, gnt = plt.subplots()
    gnt.set_title("Gráfico de Gantt - FCFS")
    gnt.set_xlabel("Tempo")
    gnt.set_ylabel("Processos")

    nomes = list(dict.fromkeys([pid for pid, _, _ in gantt]))
    gnt.set_yticks([15 + i * 10 for i in range(len(nomes))])
    gnt.set_yticklabels(nomes)
    gnt.set_ylim(0, 10 + len(nomes) * 20)

    cores = list(mcolors.TABLEAU_COLORS.values())
    cor_processos = {pid: cores[i % len(cores)] for i, pid in enumerate(nomes)}

    for i, pid in enumerate(nomes):
        y = 10 + i * 10
        for processo in gantt:
            if processo[0] == pid:
                inicio, fim = processo[1], processo[2]
                gnt.broken_barh([(inicio, fim - inicio)], (y, 9), facecolors=(cor_processos[pid]))

    caminho = f"graficos/{nome_arquivo}.png"
    plt.savefig(caminho)
    plt.close()
    print(f"Gráfico salvo em: {caminho}")
