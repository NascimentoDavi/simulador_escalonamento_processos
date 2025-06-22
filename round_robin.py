import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

def escalonar_round_robin(processos, quantum, nome_arquivo="round_robin"):
    processos = [p.copy() for p in processos]
    for p in processos:
        p['restante'] = p['burst']

    tempo = 0
    fila = []
    gantt = []
    processos_restantes = processos.copy()

    print("Round Robin - Escalonamento")
    print(f"{'Processo':<10}{'Início':<10}{'Fim':<10}")

    while processos_restantes or fila:
        # Adiciona processos que chegaram até o tempo atual
        for p in processos:
            if p['arrival'] == tempo and p not in fila and p in processos_restantes:
                fila.append(p)

        if fila:
            processo = fila.pop(0)
            inicio = tempo
            execucao = min(quantum, processo['restante'])
            tempo += execucao
            processo['restante'] -= execucao

            gantt.append((processo['id'], inicio, tempo))
            print(f"{processo['id']:<10}{inicio:<10}{tempo:<10}")

            # Adiciona processos que chegaram no meio da execução
            for p in processos:
                if inicio < p['arrival'] <= tempo and p not in fila and p in processos_restantes:
                    fila.append(p)

            if processo['restante'] > 0:
                fila.append(processo)
            else:
                processos_restantes.remove(processo)
        else:
            tempo += 1

    desenhar_gantt(gantt, nome_arquivo)

def desenhar_gantt(gantt, nome_arquivo="round_robin"):
    os.makedirs("graficos", exist_ok=True)

    fig, gnt = plt.subplots()
    gnt.set_title("Gráfico de Gantt - Round Robin")
    gnt.set_xlabel("Tempo")
    gnt.set_ylabel("Processos")

    nomes = list(dict.fromkeys([pid for pid, _, _ in gantt]))  # mantém ordem
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
