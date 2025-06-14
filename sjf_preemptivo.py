# Também conhecido como Shortest Remaining Time First (SRTF)

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def escalonar_sjf_preemptivo(processos):
    processos = [p.copy() for p in processos]  # Evita alterar original
    tempo_total = 0
    for p in processos:
        tempo_total += p['burst']
        p['restante'] = p['burst']

    tempo = 0
    gantt = []
    processo_atual = None
    inicio_execucao = None
    fila = []

    print("SJF Preemptivo (SRTF) - Escalonamento")
    print(f"{'Processo':<10}{'Início':<10}{'Fim':<10}")

    while any(p['restante'] > 0 for p in processos):

        # Filtra processos disponíveis
        disponiveis = [p for p in processos if p['arrival'] <= tempo and p['restante'] > 0]
        if disponiveis:
            # Escolhe o de menor tempo restante
            menor = min(disponiveis, key=lambda p: p['restante'])

            if processo_atual != menor:
                # Troca de processo - salva anterior
                if processo_atual is not None and inicio_execucao is not None:
                    gantt.append((processo_atual['id'], inicio_execucao, tempo))
                    print(f"{processo_atual['id']:<10}{inicio_execucao:<10}{tempo:<10}")

                processo_atual = menor
                inicio_execucao = tempo

            processo_atual['restante'] -= 1
        else:
            # Ninguém disponível, tempo avança
            if processo_atual is not None and inicio_execucao is not None:
                gantt.append((processo_atual['id'], inicio_execucao, tempo))
                print(f"{processo_atual['id']:<10}{inicio_execucao:<10}{tempo:<10}")
                processo_atual = None
                inicio_execucao = None

        tempo += 1

    # Finaliza último processo em execução
    if processo_atual is not None and inicio_execucao is not None:
        gantt.append((processo_atual['id'], inicio_execucao, tempo))
        print(f"{processo_atual['id']:<10}{inicio_execucao:<10}{tempo:<10}")

    desenhar_gantt(gantt)


def desenhar_gantt(gantt):
    fig, gnt = plt.subplots()
    gnt.set_title("Gráfico de Gantt - SJF Preemptivo (SRTF)")
    gnt.set_xlabel("Tempo")
    gnt.set_ylabel("Processos")

    gnt.set_yticks([15 + i * 10 for i in range(len(set(pid for pid, _, _ in gantt)))])
    nomes = list(dict.fromkeys([pid for pid, _, _ in gantt]))  # mantém ordem
    gnt.set_yticklabels(nomes)
    gnt.set_ylim(0, 10 + len(nomes) * 20)

    cores_disponiveis = list(mcolors.TABLEAU_COLORS.values())
    cor_processos = {pid: cores_disponiveis[i % len(cores_disponiveis)] for i, pid in enumerate(nomes)}

    for i, pid in enumerate(nomes):
        y = 10 + i * 10
        for item in gantt:
            if item[0] == pid:
                gnt.broken_barh([(item[1], item[2] - item[1])], (y, 9), facecolors=cor_processos[pid])

    plt.show()
