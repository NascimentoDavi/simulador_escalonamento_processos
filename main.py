import os
from fcfs import escalonar_fcfs
from sjf_nao_preemptivo import escalonar_sjf_naopreemptivo

# Lê arquivos com processos de entrada
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

    # Pasta com informacoes de entrada
    pasta = "entradas"

    # Arquivos da pasta
    arquivos = [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]

    if not arquivos:
        print("Nenhum arquivo encontrado na pasta")
    else:
        for nome_arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta, nome_arquivo)
            print(f"/n--- Executando {nome_arquivo} ---")

            processos = ler_entrada(caminho_arquivo)
            escalonar_fcfs(processos)