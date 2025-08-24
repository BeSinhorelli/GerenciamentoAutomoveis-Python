import os
import struct

class Automovel:
    def __init__(self, id=0, marca="", modelo="", cor="", tipo=' ', placa="", ano=0, preco=0.0, quilometragem=0):
        self.id = id
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.tipo = tipo
        self.placa = placa
        self.ano = ano
        self.preco = preco
        self.quilometragem = quilometragem

def limpar_tela():
    os.system('clear' if os.name == 'posix' else 'cls')

def adicionar_automovel():
    limpar_tela()
    automoveis = carregar_automoveis()
    
    while True:
        try:
            id = int(input("Digite o ID do veículo: "))
            if id < 0:
                print("ID negativo não pode!")
                continue
            id_existe = any(auto.id == id for auto in automoveis)
            if id_existe:
                print("ID já existente")
                continue
                
            break
        except ValueError:
            print("Digite um número válido!")
    
    marca = input("Digite a marca: ")
    modelo = input("Digite o modelo: ")
    cor = input("Digite a cor: ")
    
    while True:
        tipo = input("Digite o tipo (somente p ou u): ").lower()
        if tipo in ['p', 'u']:
            break
        print("Tipo inválido!")
    
    placa = input("Digite a placa: ")
    
    while True:
        try:
            ano = int(input("Digite o ano de fabricação: "))
            if ano >= 0:
                break
            print("Ano negativo não pode!")
        except ValueError:
            print("Digite um número válido!")
    
    while True:
        try:
            preco = float(input("Digite o preço: "))
            if preco >= 0:
                break
            print("Preço negativo não pode!")
        except ValueError:
            print("Digite um número válido!")
    
    while True:
        try:
            quilometragem = int(input("Digite a quilometragem: "))
            if quilometragem >= 0:
                break
            print("Quilometragem negativa não pode!")
        except ValueError:
            print("Digite um número válido!")
    
    novo_auto = Automovel(id, marca, modelo, cor, tipo, placa, ano, preco, quilometragem)
    automoveis.append(novo_auto)
    salvar_automoveis(automoveis)
    
    limpar_tela()
    print("Dados preenchidos!")

def listar_automoveis():
    limpar_tela()
    automoveis = carregar_automoveis()
    
    if not automoveis:
        print("Nenhum automóvel cadastrado.")
        return
    
    for i, auto in enumerate(automoveis):
        print("//------------------------------//")
        print(f"Automóvel {i}")
        print(f"ID: {auto.id}")
        print(f"Marca: {auto.marca}")
        print(f"Modelo: {auto.modelo}")
        print(f"Cor: {auto.cor}")
        print(f"Tipo: {auto.tipo}")
        print(f"Placa: {auto.placa}")
        print(f"Ano de fabricação: {auto.ano}")
        print(f"Preço: {auto.preco:.2f}")
        print(f"Quilometragem: {auto.quilometragem}")
        print("//------------------------------//\n")

def procurar_automovel():
    try:
        id = int(input("Digite o ID do carro: "))
    except ValueError:
        print("ID inválido!")
        return
    
    limpar_tela()
    automoveis = carregar_automoveis()
    
    encontrado = False
    for auto in automoveis:
        if auto.id == id:
            print("Carro encontrado!")
            print("//------------------------------//")
            print(f"ID: {auto.id}")
            print(f"Marca: {auto.marca}")
            print(f"Modelo: {auto.modelo}")
            print(f"Cor: {auto.cor}")
            print(f"Tipo: {auto.tipo}")
            print(f"Placa: {auto.placa}")
            print(f"Ano de fabricação: {auto.ano}")
            print(f"Preço: {auto.preco:.2f}")
            print(f"Quilometragem: {auto.quilometragem}")
            print("//------------------------------//")
            encontrado = True
            break
    
    if not encontrado:
        print(f"Carro com ID {id} não encontrado.")

def excluir_automovel():
    try:
        id = int(input("Digite o ID do carro a ser removido: "))
    except ValueError:
        print("ID inválido!")
        return
    
    automoveis = carregar_automoveis()
    automoveis_originais = len(automoveis)

    automoveis = [auto for auto in automoveis if auto.id != id]
    
    if len(automoveis) < automoveis_originais:
        salvar_automoveis(automoveis)
        print("Carro excluído com sucesso!")
    else:
        print("Carro não encontrado.")

def editar_automovel():
    automoveis = carregar_automoveis()
    
    if not automoveis:
        print("Nenhum automóvel cadastrado para editar.")
        return
    
    try:
        id = int(input("Digite o ID para a edição: "))
    except ValueError:
        print("ID inválido!")
        return
    
    if id < 0:
        print("ID negativo não pode!")
        return
    
    auto_editar = None
    for auto in automoveis:
        if auto.id == id:
            auto_editar = auto
            break
    
    if auto_editar is None:
        print("Automóvel não encontrado!")
        return
    
    while True:
        print("\nSelecione uma das opções abaixo para a edição:")
        print("1 - Marca")
        print("2 - Modelo")
        print("3 - Cor")
        print("4 - Tipo")
        print("5 - Placa")
        print("6 - Ano de fabricação")
        print("7 - Preço")
        print("8 - Quilometragem")
        print("9 - Editar tudo")
        print("10 - Sair")
        
        try:
            opcao = int(input("Escolha: "))
        except ValueError:
            print("Opção inválida!")
            continue
        
        if opcao == 1:
            auto_editar.marca = input("Digite a marca do carro: ")
            limpar_tela()
        elif opcao == 2:
            auto_editar.modelo = input("Digite o modelo do carro: ")
            limpar_tela()
        elif opcao == 3:
            auto_editar.cor = input("Digite a cor do carro: ")
            limpar_tela()
        elif opcao == 4:
            while True:
                tipo = input("Digite o tipo do carro (somente p ou u): ").lower()
                if tipo in ['p', 'u']:
                    auto_editar.tipo = tipo
                    break
                print("Tipo inválido!")
            limpar_tela()
        elif opcao == 5:
            auto_editar.placa = input("Digite a placa do carro: ")
            limpar_tela()
        elif opcao == 6:
            while True:
                try:
                    ano = int(input("Digite o ano de fabricação do carro: "))
                    if ano >= 0:
                        auto_editar.ano = ano
                        break
                    print("Ano negativo não pode!")
                except ValueError:
                    print("Digite um número válido!")
            limpar_tela()
        elif opcao == 7:
            while True:
                try:
                    preco = float(input("Digite o preço do carro: "))
                    if preco >= 0:
                        auto_editar.preco = preco
                        break
                    print("Preço negativo não pode!")
                except ValueError:
                    print("Digite um número válido!")
            limpar_tela()
        elif opcao == 8:
            while True:
                try:
                    quilometragem = int(input("Digite a quilometragem do carro: "))
                    if quilometragem >= 0:
                        auto_editar.quilometragem = quilometragem
                        break
                    print("Quilometragem negativa não pode!")
                except ValueError:
                    print("Digite um número válido!")
            limpar_tela()
        elif opcao == 9:
            auto_editar.marca = input("Digite a marca: ")
            auto_editar.modelo = input("Digite o modelo do carro: ")
            auto_editar.cor = input("Digite a cor do carro: ")
            
            while True:
                tipo = input("Digite o tipo do carro (somente p ou u): ").lower()
                if tipo in ['p', 'u']:
                    auto_editar.tipo = tipo
                    break
                print("Tipo inválido!")
            
            auto_editar.placa = input("Digite a placa do carro: ")
            
            while True:
                try:
                    ano = int(input("Digite o ano de fabricação do carro: "))
                    if ano >= 0:
                        auto_editar.ano = ano
                        break
                    print("Ano negativo não pode!")
                except ValueError:
                    print("Digite um número válido!")
            
            while True:
                try:
                    preco = float(input("Digite o preço do carro: "))
                    if preco >= 0:
                        auto_editar.preco = preco
                        break
                    print("Preço negativo não pode!")
                except ValueError:
                    print("Digite um número válido!")
            
            while True:
                try:
                    quilometragem = int(input("Digite a quilometragem do carro: "))
                    if quilometragem >= 0:
                        auto_editar.quilometragem = quilometragem
                        break
                    print("Quilometragem negativa não pode!")
                except ValueError:
                    print("Digite um número válido!")
            
            limpar_tela()
        elif opcao == 10:
            print("Saindo da edição...")
            break
        else:
            print("Opção inválida!")
            continue
        
        salvar_automoveis(automoveis)
    
    limpar_tela()

def carregar_automoveis():
    automoveis = []
    try:
        with open("automoveis.dat", "rb") as arquivo:
            while True:
                # Formato correto: id (i), marca (50s), modelo (50s), cor (70s), 
                # tipo (c), placa (10s), ano (i), preco (f), quilometragem (i)
                formato = "i50s50s70sc10sifi"
                tamanho_registro = struct.calcsize(formato)
                
                dados = arquivo.read(tamanho_registro)
                if not dados or len(dados) < tamanho_registro:
                    break
                # Desempacotar os dados
                registro = struct.unpack(formato, dados)
                
                id = registro[0]
                marca = registro[1].decode('utf-8').rstrip('\x00')
                modelo = registro[2].decode('utf-8').rstrip('\x00')
                cor = registro[3].decode('utf-8').rstrip('\x00')
                tipo = registro[4].decode('utf-8')
                placa = registro[5].decode('utf-8').rstrip('\x00')
                ano = registro[6]
                preco = registro[7]
                quilometragem = registro[8]
                
                auto = Automovel(id, marca, modelo, cor, tipo, placa, ano, preco, quilometragem)
                automoveis.append(auto)
    except FileNotFoundError:
        pass 
    
    return automoveis

def salvar_automoveis(automoveis):
    with open("automoveis.dat", "wb") as arquivo:
        for auto in automoveis:
            marca = auto.marca.ljust(50, '\x00').encode('utf-8')
            modelo = auto.modelo.ljust(50, '\x00').encode('utf-8')
            cor = auto.cor.ljust(70, '\x00').encode('utf-8')
            tipo = auto.tipo.encode('utf-8')
            placa = auto.placa.ljust(10, '\x00').encode('utf-8')

            formato = "i50s50s70sc10sifi"
            dados = struct.pack(formato, 
                               auto.id, 
                               marca, 
                               modelo, 
                               cor, 
                               tipo, 
                               placa, 
                               auto.ano, 
                               auto.preco, 
                               auto.quilometragem)
            arquivo.write(dados)

def main():
    limpar_tela()
    
    while True:
        print("\nDigite uma opção:")
        print("1 - Adicionar um automóvel")
        print("2 - Listar todos os automóveis")
        print("3 - Procurar automóvel específico")
        print("4 - Excluir um automóvel")
        print("5 - Editar um automóvel")
        print("0 - Sair")
        
        try:
            opcao = int(input("Escolha: "))
        except ValueError:
            print("Opção inválida!")
            continue
        
        if opcao == 1:
            adicionar_automovel()
        elif opcao == 2:
            listar_automoveis()
        elif opcao == 3:
            procurar_automovel()
        elif opcao == 4:
            excluir_automovel()
        elif opcao == 5:
            editar_automovel()
        elif opcao == 0:
            print("Finalizando...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()