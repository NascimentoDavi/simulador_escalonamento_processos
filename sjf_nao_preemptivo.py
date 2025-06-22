import matplotlib.pyplot as plt
import os

def escalonar_sjf_naopreemptivo(processos, nome_arquivo="sjf_nao_preemptivo"):
    processos = processos.copy()  # Não altera a lista original
    n = len(processos)
    tempo_atual = 0
    gantt = []
    processos_executados = set()

    print('SJF - Escalonamento Não Preemptivo')
    print(f"{'Processo':<10}{'Início':<10}{'Fim':<10}{'Espera':<10}{'Turnaround'}")

    while len(processos_executados) < n:
        disponiveis = [p for p in processos if p['arrival'] <= tempo_atual and p['id'] not in processos_executados]

        if disponiveis:
            atual = min(disponiveis, key=lambda p: p['burst'])
            inicio = max(tempo_atual, atual['arrival'])
            fim = inicio + atual['burst']
            espera = inicio - atual['arrival']
            turnaround = fim - atual['arrival']

            gantt.append((atual['id'], inicio, fim))

            tempo_atual = fim
            processos_executados.add(atual['id'])

            print(f"{atual['id']:<10}{inicio:<10}{fim:<10}{espera:<10}{turnaround}")
        else:
            proximo = min([p for p in processos if p['id'] not in processos_executados], key=lambda p: p['arrival'])
            tempo_atual = proximo['arrival']

    desenhar_gantt(gantt, nome_arquivo)

def desenhar_gantt(gantt, nome_arquivo="sjf_nao_preemptivo"):
    import matplotlib.colors as mcolors
    os.makedirs("graficos", exist_ok=True)

    fig, gnt = plt.subplots()
    gnt.set_title("Gráfico de Gantt - SJF Não Preemptivo")
    gnt.set_xlabel("Tempo")
    gnt.set_ylabel("Processos")

    gnt.set_yticks([15 + i*10 for i in range(len(gantt))])
    gnt.set_yticklabels([processo[0] for processo in gantt])
    gnt.set_ylim(0, 10 + len(gantt)*20)

    cores = list(mcolors.TABLEAU_COLORS.values())

    for i, (pid, inicio, fim) in enumerate(gantt):
        cor = cores[i % len(cores)]
        gnt.broken_barh([(inicio, fim - inicio)], (10 + i*10, 9), facecolors=cor)

    caminho = f"graficos/{nome_arquivo}.png"
    plt.savefig(caminho)
    plt.close()
    print(f"Gráfico salvo em: {caminho}")
