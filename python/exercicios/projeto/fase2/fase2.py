import csv
import matplotlib.pyplot as plt
from datetime import datetime
import os
import sys

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_dados(nome_arquivo):
    dados = []
    if not os.path.exists(nome_arquivo):
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return dados
    
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            primeira_linha = f.readline()
        
        # Detecta o delimitador
        if ';' in primeira_linha:
            delimiter = ';'
        elif ',' in primeira_linha:

            delimiter = ','
        else:
            delimiter = '\t'  # tab como fallback
        print(f"Detectado delimitador: '{delimiter}'")
        
        # Tenta diferentes encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252']
        
        for encoding in encodings:
            try:
                with open(nome_arquivo, "r", encoding=encoding) as f:
                    leitor = csv.DictReader(f, delimiter=delimiter)
                    cabecalhos = leitor.fieldnames
                    print(f"Encoding: {encoding}, Cabeçalhos: {cabecalhos}")
                    
                    # Reinicia a leitura para processar todos os dados
                    f.seek(0)
                    next(leitor) 
                    
                    for linha in leitor:
                        try:

                            try:
                                data_obj = datetime.strptime(linha["data"], "%d/%m/%Y")
                            except ValueError:
                                try:
                                    data_obj = datetime.strptime(linha["data"], "%Y-%m-%d")
                                except ValueError:
                                    data_obj = datetime.strptime(linha["data"], "%m/%d/%Y")
                        
                            precip = float(linha["precip"].replace(',', '.')) if linha["precip"] else 0.0
                            maxima = float(linha["maxima"].replace(',', '.')) if linha["maxima"] else 0.0
                            minima = float(linha["minima"].replace(',', '.')) if linha["minima"] else 0.0
                            um_relativa = float(linha["um_relativa"].replace(',', '.')) if linha["um_relativa"] else 0.0
                            vel_vento = float(linha["vel_vento"].replace(',', '.')) if linha["vel_vento"] else 0.0
                            dados.append({
                                "data": data_obj,
                                "precip": precip,
                                "maxima": maxima,
                                "minima": minima,
                                "um_relativa": um_relativa,
                                "vel_vento": vel_vento
                            })
                        except (ValueError, KeyError) as e:
                            print(f"Erro ao processar linha: {linha}. Erro: {e}")
                            continue
                
                print(f"Sucesso com encoding: {encoding}")
                limpar_tela()
                break
                
            except UnicodeDecodeError:
                print(f"Falha com encoding: {encoding}")
                continue
            except Exception as e:
                print(f"Erro inesperado com encoding {encoding}: {e}")
                continue
        
        print(f"Total de registros carregados: {len(dados)}")
        
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
    
    return dados

# --------------------
# (a) Visualização por intervalo de dados
# --------------------
def visualizar_intervalo(dados, mes_ini, ano_ini, mes_fim, ano_fim, opcao):
    print("\n===== RESULTADO =====")
    
    # Filtra os dados pelo intervalo
    dados_filtrados = []
    for d in dados:
        data = d["data"]
        if (ano_ini < data.year < ano_fim) or \
           (data.year == ano_ini and data.month >= mes_ini) or \
           (data.year == ano_fim and data.month <= mes_fim):
            dados_filtrados.append(d)
    
    if not dados_filtrados:
        print("Nenhum dado encontrado para o período especificado.")
        return
    
    # Exibe os dados conforme a opção
    if opcao == 1:
        print("Data        | Precip (mm) | Máx (°C) | Mín (°C) | Umidade (%) | Vento (m/s)")
        print("-" * 80)
        for d in dados_filtrados:
            print(f"{d['data'].strftime('%d/%m/%Y')} | {d['precip']:10.2f} | {d['maxima']:8.2f} | {d['minima']:7.2f} | {d['um_relativa']:11.2f} | {d['vel_vento']:10.2f}")
    
    elif opcao == 2:
        print("Data        | Precip (mm)")
        print("-" * 30)
        for d in dados_filtrados:
            print(f"{d['data'].strftime('%d/%m/%Y')} | {d['precip']:10.2f}")
    
    elif opcao == 3:
        print("Data        | Máx (°C) | Mín (°C)")
        print("-" * 40)
        for d in dados_filtrados:
            print(f"{d['data'].strftime('%d/%m/%Y')} | {d['maxima']:8.2f} | {d['minima']:7.2f}")
    
    elif opcao == 4:
        print("Data        | Umidade (%) | Vento (m/s)")
        print("-" * 45)
        for d in dados_filtrados:
            print(f"{d['data'].strftime('%d/%m/%Y')} | {d['um_relativa']:11.2f} | {d['vel_vento']:10.2f}")

# --------------------
# Mês mais chuvoso
# --------------------
def mes_mais_chuvoso(dados):
    precipitacoes = {}
    for d in dados:
        chave = (d["data"].month, d["data"].year)
        precipitacoes[chave] = precipitacoes.get(chave, 0) + d["precip"]

    if not precipitacoes:
        print("Nenhum dado disponível para calcular o mês mais chuvoso.")
        return

    mais_chuvoso = max(precipitacoes, key=precipitacoes.get)
    mes_nome = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
                "Jul", "Ago", "Set", "Out", "Nov", "Dez"][mais_chuvoso[0] - 1]
    
    print(f"\nMês mais chuvoso: {mes_nome}/{mais_chuvoso[1]}")
    print(f"Precipitação total: {precipitacoes[mais_chuvoso]:.2f} mm")

# --------------------
# (c) Média da temp. mínima por ano (2006-2016)
# --------------------
def medias_minimas_mes(dados, mes):
    medias = {}
    for ano in range(2006, 2017):
        valores = [d["minima"] for d in dados if d["data"].year == ano and d["data"].month == mes]
        if valores:
            medias[ano] = sum(valores) / len(valores)
    return medias

# --------------------
# Gráfico
# --------------------
def grafico_medias(medias, mes):
    if not medias:
        print("Sem dados para gerar gráfico.")
        return
    
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    anos = list(medias.keys())
    valores = list(medias.values())

    plt.figure(figsize=(10, 6))
    bars = plt.bar([str(ano) for ano in anos], valores, color="skyblue", edgecolor="black")
    
    for bar, valor in zip(bars, valores):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{valor:.1f}°C', ha='center', va='bottom')
    
    plt.title(f"Médias da temperatura mínima em {meses[mes-1]} (2006-2016)")
    plt.xlabel("Ano")
    plt.ylabel("Temperatura mínima média (°C)")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# --------------------
# Média geral
# --------------------
def media_geral(medias):
    if not medias:
        return None
    return sum(medias.values()) / len(medias)

# --------------------
# Funções para validação
# --------------------
def validar_mes(mes):
    try:
        mes = int(mes)
        if 1 <= mes <= 12:
            return mes
        else:
            return None
    except ValueError:
        return None

def validar_ano(ano):
    try:
        ano = int(ano)
        if 1961 <= ano <= 2016:
            return ano
        else:
            return None
    except ValueError:
        return None

# --------------------
# PROGRAMA PRINCIPAL
# --------------------
if __name__ == "__main__":
    pasta_script = os.path.dirname(os.path.abspath(__file__))

    arquivo = input("Digite o nome do arquivo CSV (nome: anexo.csv): ").strip()
    if not arquivo:
        arquivo = "anexo.csv"
    caminho_arquivo = os.path.join(pasta_script, arquivo)

    print(f"Procurando em: {caminho_arquivo}")
    print(f"Arquivo existe? {os.path.exists(caminho_arquivo)}")
    limpar_tela()
    dados = carregar_dados(caminho_arquivo)
    if not dados:
        print("Nenhum dado carregado. Verifique o arquivo e tente novamente.")
        sys.exit(1)

    # Menu principal
    while True:
        print("\n" + "="*50)
        print("ANÁLISE DE DADOS METEOROLÓGICOS - PORTO ALEGRE")
        print("="*50)
        print("1. Visualizar intervalo de dados")
        print("2. Encontrar mês mais chuvoso")
        print("3. Médias de temperatura mínima por mês (2006-2016)")
        print("4. Sair")
        
        opcao_principal = input("\nEscolha uma opção (1-4): ").strip()
        
        if opcao_principal == "1":
            limpar_tela()
            print("\n--- VISUALIZAÇÃO POR INTERVALO ---")
            
            mes_ini = validar_mes(input("Mês inicial (1-12): "))
            ano_ini = validar_ano(input("Ano inicial (1961-2016): "))
            mes_fim = validar_mes(input("Mês final (1-12): "))
            ano_fim = validar_ano(input("Ano final (1961-2016): "))
            
            if not all([mes_ini, ano_ini, mes_fim, ano_fim]):
                print("Entrada inválida. Tente novamente.")
                continue
            
            print("\nTipo de dados:")
            print("1. Todos os dados")
            print("2. Apenas precipitação")
            print("3. Apenas temperatura")
            print("4. Apenas umidade e vento")
            
            tipo_dados = input("Escolha o tipo de dados (1-4): ").strip()
            if tipo_dados not in ["1", "2", "3", "4"]:
                print("Opção inválida.")
                continue
            
            visualizar_intervalo(dados, mes_ini, ano_ini, mes_fim, ano_fim, int(tipo_dados))
            
        elif opcao_principal == "2":
            limpar_tela()
            print("\n--- MÊS MAIS CHUVOSO ---")
            mes_mais_chuvoso(dados)
            
        elif opcao_principal == "3":
            limpar_tela()
            print("\n--- ANÁLISE DE TEMPERATURAS MÍNIMAS (2006-2016) ---")
            
            mes = validar_mes(input("Digite o mês para análise (1-12): "))
            if not mes:
                print("Mês inválido.")
                continue
            
            medias = medias_minimas_mes(dados, mes)
            
            if medias:
                print(f"\nMédias de temperatura mínima para o mês {mes}:")
                for ano, media in medias.items():
                    print(f"{ano}: {media:.2f}°C")
                
                #Média
                media_geral_valor = media_geral(medias)
                if media_geral_valor is not None:
                    print(f"\nMédia geral: {media_geral_valor:.2f}°C")
                
                #Gráfico
                gerar_grafico = input("\nDeseja gerar o gráfico? (s/n): ").strip().lower()
                if gerar_grafico == 's' or gerar_grafico == 'S':
                    grafico_medias(medias, mes)
            elif gerar_grafico == 'n' or gerar_grafico == 'N':
                print("Não há dados para o mês especificado no período 2006-2016.")
            else:
                print("Opção inválida.")
                
        elif opcao_principal == "4":
            limpar_tela()
            print("Saindo do programa...")
            break
            
        else:
            print("Opção inválida. Tente novamente.")