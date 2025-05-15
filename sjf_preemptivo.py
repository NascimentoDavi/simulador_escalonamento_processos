import matplotlib.pyplot as plt

def escalonar_sjf_preemptivo(processos):
    processos = [p.copy() for p in processos] # Cópia para não alterar a original

    n = len(processos)
    
    tempo_atual = 0
    
    tempo_restante = {p['id']: p['burst'] for p in processos}
    
    gantt = []

    inicio_execucao = {}

    fim_execucao = {}

    pronto = []

    processo_atual = None
    log_execucao = [] # Para o gráfico

    while True:
        # Verifica se novos processs chegaram nesse instante
        for p in processos:
            if p['arrival'] == tempo_tempo_atual:
                pronto.append(p)

        # Remove processos finalizados da lista pronta
        pronto = [p for p in pronto if tempo_restante[p['id']] > 0]

        # Seleciona o processo com menor tempo restante
        if pronto:
            processo_com_menor_restante = min(pronto, key=lambda p: tempo_restante[p['id']])
        else:
            processo_com_menor_restante = None

        if processo_com_menor_restante:
            pid = processo_com_menor_restante['id']

            if processo_atual != pid:
                if processo_atual is not None:
                    # Finaliza execução do processo anterior no gráfico
                    log_execucao[-1]['fim'] = tempo_atual

                # Começa novo processo
                log_execucao.append({'pid': pid, 'inicio': tempo_atual, 'fim': None})

                if pid not in inicio_execucao:
                    inicio_execucao[pid] = tempo_atual

                processo_atual = pid

            tempo_restante[pid] -= 1

            if tempo_restante[pid] == 0:
                fim_execucao[pid] = tempo_atual + 1
                processo_atual = None

        else:
            # CPU ociosa
            if processo_atual is not None:
                log_execucao[-1]['fim'] = tempo_atual
                processo_atual = None

        tempo_atual += 1

        if all(tempo_restante[pid] == 0 for pid in tempo_restante):
            if processo_atual:
                log_execucao[-1]['fim'] = tempo_atual
            break

    # Calcula e imprime métricas
    print('SJF Preemptivo - Escalonamento')
    print(f"{'Processo':<10}{'Início':<10}{'Fim':<10}{'Espera':<10}{'Turnaround'}")
    for p in processos:
        pid = p['id']
        inicio = inicio_execucao[pid]
        fim = fim_execucao[pid]
        turnaround = fim - p['arrival']
        espera = turnaround - p['burst']
        gantt.append((pid, inicio, fim))
        print(f"{pid:<10}{inicio:<10}{fim:<10}{espera:<10}{turnaround}")

    desenhar_gantt_execucoes(log_execucao)

def desenhar_gantt_execucoes(exec_log):
    fig, gnt = plt.subplots()
    gnt.set_title("Gráfico de Gantt - SJF Preemptivo")
    gnt.set_xlabel("Tempo")
    gnt.set_ylabel("Processos")

    processos_unicos = list({log['pid'] for log in exec_log})
    y_ticks = [15 + i*10 for i in range(len(processos_unicos))]
    gnt.set_yticks(y_ticks)
    gnt.set_yticklabels(processos_unicos)
    gnt.set_ylim(0, 10 + len(processos_unicos)*20)

    cores_disponiveis = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
    cor_map = {pid: cores_disponiveis[i % len(cores_disponiveis)] for i, pid in enumerate(processos_unicos)}

    for i, pid in enumerate(processos_unicos):
        for log in exec_log:
            if log['pid'] == pid and log['fim'] is not None:
                gnt.broken_barh([(log['inicio'], log['fim'] - log['inicio'])], (10 + i*10, 9), facecolors=(cor_map[pid]))

    plt.show()