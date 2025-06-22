import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

def escalonar_multifilas(processos, nome_arquivo="multifilas"):
    processos = [p.copy() for p in processos]
    for p in processos:
        p['restante'] = p['burst']
        p['fila'] = 0  # Começa na fila 0

    tempo = 0
    gantt = []
    processos_restantes = processos.copy()
    fila = []

    print("Escalonamento Múltiplas Filas")
    print(f"{'Processo':<10}{'Início':<10}{'Fim':<10}{'Fila':<10}")

    while processos_restantes or fila:
        # Adiciona processos que chegaram até agora
        for p in processos:
            if p['arrival'] == tempo and p not in fila and p in processos_restantes:
                fila.append(p)

        if fila:
            # Ordena os processos por menor fila (mais prioritária)
            fila.sort(key=lambda p: (p['fila'], p['arrival']))

            processo = fila.pop(0)
            quantum = 2 ** processo['fila']
            inicio = tempo
            execucao = min(quantum, processo['restante'])
            tempo += execucao
            processo['restante'] -= execucao

            gantt.append((processo['id'], inicio, tempo))
            print(f"{processo['id']:<10}{inicio:<10}{tempo:<10}{processo['fila']:<10}")

            # Adiciona processos que chegaram durante a execução
            for p in processos:
                if inicio < p['arrival'] <= tempo and p not in fila and p in processos_restantes:
                    fila.append(p)

            if processo['restante'] > 0:
                processo['fila'] += 1  # Rebaixa de fila
                fila.append(processo)
            else:
                processos_restantes.remove(processo)
        else:
            tempo += 1

    desenhar_gantt(gantt, nome_arquivo)

def desenhar_gantt(gantt, nome_arquivo="multifilas"):
    os.makedirs("graficos", exist_ok=True)

    fig, gnt = plt.subplots()
    gnt.set_title("Gráfico de Gantt - Múltiplas Filas")
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
