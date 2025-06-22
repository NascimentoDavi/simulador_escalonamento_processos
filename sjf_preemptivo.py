# Também conhecido como Shortest Remaining Time First (SRTF)

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

def escalonar_sjf_preemptivo(processos, nome_arquivo="sjf_preemptivo"):
    processos = [p.copy() for p in processos]
    for p in processos:
        p['restante'] = p['burst']

    tempo = 0
    gantt = []
    processo_atual = None
    inicio_execucao = None

    print("SJF Preemptivo (SRTF) - Escalonamento")
    print(f"{'Processo':<10}{'Início':<10}{'Fim':<10}")

    while any(p['restante'] > 0 for p in processos):

        # Filtra processos disponíveis
        disponiveis = [p for p in processos if p['arrival'] <= tempo and p['restante'] > 0]
        if disponiveis:
            menor = min(disponiveis, key=lambda p: p['restante'])

            if processo_atual != menor:
                if processo_atual is not None and inicio_execucao is not None:
                    gantt.append((processo_atual['id'], inicio_execucao, tempo))
                    print(f"{processo_atual['id']:<10}{inicio_execucao:<10}{tempo:<10}")
                processo_atual = menor
                inicio_execucao = tempo

            processo_atual['restante'] -= 1
        else:
            if processo_atual is not None and inicio_execucao is not None:
                gantt.append((processo_atual['id'], inicio_execucao, tempo))
                print(f"{processo_atual['id']:<10}{inicio_execucao:<10}{tempo:<10}")
                processo_atual = None
                inicio_execucao = None

        tempo += 1

    # Finaliza o último processo em execução
    if processo_atual is not None and inicio_execucao is not None:
        gantt.append((processo_atual['id'], inicio_execucao, tempo))
        print(f"{processo_atual['id']:<10}{inicio_execucao:<10}{tempo:<10}")

    desenhar_gantt(gantt, nome_arquivo)

def desenhar_gantt(gantt, nome_arquivo="sjf_preemptivo"):
    os.makedirs("graficos", exist_ok=True)

    fig, gnt = plt.subplots()
    gnt.set_title("Gráfico de Gantt - SJF Preemptivo (SRTF)")
    gnt.set_xlabel("Tempo")
    gnt.set_ylabel("Processos")

    nomes = list(dict.fromkeys([pid for pid, _, _ in gantt]))
    gnt.set_yticks([15 + i * 10 for i in range(len(nomes))])
    gnt.set_yticklabels(nomes)
    gnt.set_ylim(0, 10 + len(nomes) * 20)

    cores_disponiveis = list(mcolors.TABLEAU_COLORS.values())
    cor_processos = {pid: cores_disponiveis[i % len(cores_disponiveis)] for i, pid in enumerate(nomes)}

    for i, pid in enumerate(nomes):
        y = 10 + i * 10
        for item in gantt:
            if item[0] == pid:
                gnt.broken_barh([(item[1], item[2] - item[1])], (y, 9), facecolors=cor_processos[pid])

    caminho = f"graficos/{nome_arquivo}.png"
    plt.savefig(caminho)
    plt.close()
    print(f"Gráfico salvo em: {caminho}")
