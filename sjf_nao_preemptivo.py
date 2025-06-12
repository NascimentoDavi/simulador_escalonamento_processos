# SJF - Shortest Job First

# O escalonador sempre escolhe o processo com menor burst time (tempo de execução) dentre os processos que já chegaram

# Quando um processo começa a ser executado, ele é executado até o fim

import matplotlib.pyplot as plt

def escalonar_sjf_naopreemptivo(processos):
    processos = processos.copy()  # Não altera a lista original
    n = len(processos)
    tempo_atual = 0
    gantt = []  # armazena as informações de tempo de execução de cada processo
    processos_executados = set() # Cria um conjunto vazio - Coleção não ordenada de elementos únicos | Serve para controlar quais processos já foram executados.

    print('SJF - Escalonamento')
    print(f"{'Processo':<10}{'Início':<10}{'Fim':<10}{'Espera':<10}{'Turnaround'}")

    while len(processos_executados) < n:

        # Filtra processos que já chegaram e ainda não executaram
        disponiveis = [p for p in processos if p['arrival'] <= tempo_atual and p['id'] not in processos_executados]
        
        if disponiveis:
            # Escolhe o de menor burst (tempo de execução)
            atual = min(disponiveis, key=lambda p: p['burst'])

            # Indica quando o processo pode começar a ser executado
            inicio = max(tempo_atual, atual['arrival'])

            # Calcula quando o processo vai terminar sua execução            
            fim = inicio + atual['burst']

            espera = inicio - atual['arrival']

            # Tempo desde que chega até terminar sua execução
            turnaround = fim - atual['arrival']

            gantt.append((atual['id'], inicio, fim))

            # Tempo que último processo termina = tempo de início do processo seguinte
            tempo_atual = fim

            # Adiciona o processo atual ao conjunto de processos executados
            processos_executados.add(atual['id'])
        
            print(f"{atual['id']:<10}{inicio:<10}{fim:<10}{espera:<10}{turnaround}")

        else:
            
            # Se não tem processo disponível, avança o tempo para próximo processo que vai chegar
            proximo = min([p for p in processos if p['id'] not in processos_executados], key=lambda p: p['arrival'])
            tempo_atual = proximo['arrival']

    desenhar_gantt(gantt)

def desenhar_gantt(gantt):
    import matplotlib.colors as mcolors

    fig, gnt = plt.subplots()
    gnt.set_title("Gráfico de Gantt - SJF N Preemptivo")
    gnt.set_xlabel("Tempo")
    gnt.set_ylabel("Processos")

    gnt.set_yticks([15 + i*10 for i in range(len(gantt))])
    gnt.set_yticklabels([processo[0] for processo in gantt])
    gnt.set_ylim(0, 10 + len(gantt)*20)

    cores = list(mcolors.TABLEAU_COLORS.values())

    for i, (pid, inicio, fim) in enumerate(gantt):
        cor = cores[i %  len(cores)]
        gnt.broken_barh([(inicio, fim - inicio)], (10 + i*10, 9), facecolors=(cor))

    plt.show()