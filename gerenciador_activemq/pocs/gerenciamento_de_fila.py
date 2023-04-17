def modo_exemplo_gerente_da_fila():
    print("Iniciando gerente...")

    executando: bool = True
    while executando:
        try:
            print("==================================================")
            print("1 - Listar filas e quantidades de mensagens")
            print("2 - Listar topicos e quantidades de mensagens")
            print("3 - Criar fila")
            print("4 - Remover fila")
            print("5 - Criar tópico")
            print("6 - Remover tópico")
            print("0 - Sair")
            print("==================================================")

            opcao: str = input("Escolha uma opção: ")

            if opcao == "1":
                ...
            elif opcao == "2":
                ...
            elif opcao == "3":
                ...
            elif opcao == "4":
                ...
            elif opcao == "5":
                ...
            elif opcao == "6":
                ...
            elif opcao == "0":
                executando = False
            else:
                print("Opção inválida")
        except KeyboardInterrupt:
            executando = False

    print("Encerrando gerente...")


def modo_exemplo_cliente_da_fila():
    print(f"cliente")
