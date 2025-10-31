LIMITE_SAQUES = 3
AGENCIA = "0001"


def menu():
    menu = """
    --> Menu:
    [d]  Deposito
    [s]  Saque
    [e]  Extrato
    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Usuario
    [q]  Sair
    """
    return input(menu).lower()


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Deposito:\tR$ {valor:.2f}\n"
        print("\n--> Deposito realizado com sucesso!")
    else:
        print("\n--> Operacao falhou! O valor informado eh invalido.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n--> A operacao falhou! Voce nao tem saldo suficiente.")
    elif excedeu_limite:
        print(
            "\n--> A operacao falhou! O valor do saque excede o limite permitido."
        )
    elif excedeu_saques:
        print("\n--> A operacao falhou! Numero maximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n--> Saque realizado com sucesso!")
    else:
        print("\n--> A operacao falhou! Valor informado invalido.")

    return saldo, extrato, numero_saques


def print_extrato(saldo, /, *, extrato):
    print("\n--> Extrato:")
    print("Nao ha movimentacoes a serem exibidas." if not extrato else extrato)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("\\/\\/\\/\\/\\/ ")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [
        usuario for usuario in usuarios if usuario["cpf"] == cpf
    ]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente numeros): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n--> Ja existe usuario com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereco (logradouro, nro - bairro - cidade/sigla estado): "
    )

    usuarios.append(
        {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco,
        }
    )

    print("\n--> Usuario criado com sucesso!")


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuario: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n--> Conta criada com sucesso!")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
        }

    print("\n--> Usuario nao encontrado, fluxo de criacao de conta encerrado!")


def listar_contas(contas):
    if not contas:
        print("\n--> Nao ha contas cadastradas.")
        return

    for conta in contas:
        linha = f"""
        Agencia:\t{conta['agencia']}
        Conta:\t\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(linha)


def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opc = menu()

        match opc:
            case "d":
                try:
                    valor = float(input("Informe o valor do deposito: "))
                except ValueError:
                    print("\n--> Valor invalido, tente novamente.")
                    continue

                saldo, extrato = depositar(saldo, valor, extrato)

            case "s":
                try:
                    valor = float(input("Informe o valor do saque: "))
                except ValueError:
                    print("\n--> Valor invalido, tente novamente.")
                    continue

                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )

            case "e":
                print_extrato(saldo, extrato=extrato)

            case "nu":
                criar_usuario(usuarios)

            case "nc":
                numero_conta = len(contas) + 1
                conta = criar_conta(AGENCIA, numero_conta, usuarios)
                if conta:
                    contas.append(conta)

            case "lc":
                listar_contas(contas)

            case "q":
                print("\n--> Saindo do sistema... Ate logo!")
                print_extrato(saldo, extrato=extrato)
                break

            case _:
                print("\n--> Operacao invalida, tente novamente.")


if __name__ == "__main__":
    main()
