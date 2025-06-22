import os
from fcfs import escalonar_fcfs
from sjf_nao_preemptivo import escalonar_sjf_naopreemptivo
from sjf_preemptivo import escalonar_sjf_preemptivo
from round_robin import escalonar_round_robin
from prioridade_round_robin import escalonar_prioridade_round_robin
from multifilas import escalonar_multifilas

# Cria a pasta de grafico, se não existir
os.makedirs("graficos", exist_ok=True)

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
    pasta = "entradas"
    arquivos = [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]

    if not arquivos:
        print("Nenhum arquivo encontrado na pasta.")
    else:
        for nome_arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta, nome_arquivo)
            nome_base = os.path.splitext(nome_arquivo)[0]
            print(f"\n--- Executando {nome_arquivo} ---")

            processos = ler_entrada(caminho_arquivo)

            # Executa todos os algoritmos, passando o nome para salvar o gráfico
            escalonar_fcfs([p.copy() for p in processos], f"{nome_base}_fcfs")
            escalonar_sjf_naopreemptivo([p.copy() for p in processos], f"{nome_base}_sjf_np")
            escalonar_sjf_preemptivo([p.copy() for p in processos], f"{nome_base}_sjf_p")
            escalonar_round_robin([p.copy() for p in processos], quantum=2, nome_arquivo=f"{nome_base}_rr")
            escalonar_prioridade_round_robin([p.copy() for p in processos], quantum=2, nome_arquivo=f"{nome_base}_rr_prioridade")
            escalonar_multifilas([p.copy() for p in processos], nome_arquivo=f"{nome_base}_multifilas")
