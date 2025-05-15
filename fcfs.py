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


# # ERRO COMUM:
# qt.glx: qglx_findConfig: Failed to finding matching FBConfig for QSurfaceFormat(version 2.0, options QFlags<QSurfaceFormat::FormatOption>(), depthBufferSize -1, redBufferSize 1, greenBufferSize 1, blueBufferSize 1, alphaBufferSize -1, stencilBufferSize -1, samples -1, swapBehavior QSurfaceFormat::SingleBuffer, swapInterval 1, colorSpace QSurfaceFormat::DefaultColorSpace, profile  QSurfaceFormat::NoProfile)
# No XVisualInfo for format QSurfaceFormat(version 2.0, options QFlags<QSurfaceFormat::FormatOption>(), depthBufferSize -1, redBufferSize 1, greenBufferSize 1, blueBufferSize 1, alphaBufferSize -1, stencilBufferSize -1, samples -1, swapBehavior QSurfaceFormat::SingleBuffer, swapInterval 1, colorSpace QSurfaceFormat::DefaultColorSpace, profile  QSurfaceFormat::NoProfile)
# Falling back to using screens root_visual

# Este erro ocorre quando o QT não encontra a configuração gráfica ideal para usar o OpenGL na máquina.
# Matplotlib usa um backend em QT(Qt5Agg ou Qt6Agg) e o QT chama OpenGL