import csv
import datetime

def salvar_informacoes(peso, distancia, area):
    # Obtém a data e hora atual
    data_hora = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    # Dados a serem salvos
    dados = {
        "Peso": peso,
        "Área": area,
        "Distância": distancia,
        "Data e hora": data_hora
    }

    # Verifica se o arquivo CSV já existe ou não
    arquivo_existe = True
    try:
        with open("informacoes.csv", "r") as file:
            pass
    except FileNotFoundError:
        arquivo_existe = False

    # Abre o arquivo CSV em modo de escrita, criando-o se ainda não existir
    with open("informacoes.csv", "a", newline="") as file:
        # Define os nomes das colunas
        colunas = ["Peso", "Área", "Distância", "Data e hora"]

        # Cria o escritor CSV com tabulação como delimitador
        writer = csv.DictWriter(file, fieldnames=colunas, delimiter='\t')

        # Se o arquivo não existia antes, escreve os nomes das colunas
        if not arquivo_existe:
            writer.writeheader()

        # Escreve os dados
        writer.writerow(dados)
