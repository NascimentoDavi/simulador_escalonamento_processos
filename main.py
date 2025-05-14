from fcfs import escalonar_fcfs

def ler_entrada(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    num_processos = int(linhas[0])

    processos = []

    for linha in linhas[1:num_processos+1]:
        pid, chegada, duracao, prioridade = linha.strip().split()

        processos.append({
            'id': pid,
            'arrival': int(chegada),
            'burst': int(duracao),
            'priority': int(prioridade)
        })
        
    return processos

if __name__ == '__main__':
    processos = ler_entrada("entrada.txt")
    escalonar_fcfs(processos)