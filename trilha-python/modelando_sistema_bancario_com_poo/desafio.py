from abc import ABC, abstractmethod
from datetime import datetime

LIMITE_SAQUES = 3
AGENCIA = "0001"


class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = AGENCIA
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("\n--> Valor invalido.")
            return False
        if valor > self._saldo:
            print("\n--> Saldo insuficiente.")
            return False
        self._saldo -= valor
        print("\n--> Saque realizado com sucesso!")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n--> Valor invalido.")
            return False
        self._saldo += valor
        print("\n--> Deposito realizado com sucesso!")
        return True

    def __str__(self):
        return f"Agencia:\t{self.agencia}\nConta:\t\t{self.numero}\nTitular:\t{self.cliente.nome}"


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=LIMITE_SAQUES):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([t for t in self.historico.transacoes if t["tipo"] == "Saque"])
        if valor > self.limite:
            print("\n--> Valor excede o limite de saque.")
            return False
        if numero_saques >= self.limite_saques:
            print("\n--> Numero maximo de saques excedido.")
            return False
        return super().sacar(valor)


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {"tipo": transacao.__class__.__name__, "valor": transacao.valor,
             "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def menu():
    return input("""
    --> Menu:
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Usuario
    [q]  Sair
    """).lower()


def filtrar_cliente(cpf, clientes):
    return next((c for c in clientes if c.cpf == cpf), None)


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n--> Cliente nao possui conta.")
        return None
    return cliente.contas[0]


def listar_contas(contas):
    if not contas:
        print("\n--> Nao ha contas cadastradas.")
        return
    for conta in contas:
        print("=" * 100)
        print(conta)


def exibir_extrato(conta):
    print("\n--> Extrato:")
    if not conta.historico.transacoes:
        print("Nao ha movimentacoes.")
    else:
        for t in conta.historico.transacoes:
            print(f"{t['tipo']}:\tR$ {t['valor']:.2f}\t({t['data']})")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}\n")


def main():
    clientes, contas = [], []

    while True:
        opc = menu()

        match opc:
            case "d":
                cpf = input("CPF do cliente: ")
                cliente = filtrar_cliente(cpf, clientes)
                if not cliente:
                    print("\n--> Cliente nao encontrado.")
                    continue
                conta = recuperar_conta_cliente(cliente)
                if not conta:
                    continue
                try:
                    valor = float(input("Valor do deposito: "))
                except ValueError:
                    print("\n--> Valor invalido.")
                    continue
                cliente.realizar_transacao(conta, Deposito(valor))

            case "s":
                cpf = input("CPF do cliente: ")
                cliente = filtrar_cliente(cpf, clientes)
                if not cliente:
                    print("\n--> Cliente nao encontrado.")
                    continue
                conta = recuperar_conta_cliente(cliente)
                if not conta:
                    continue
                try:
                    valor = float(input("Valor do saque: "))
                except ValueError:
                    print("\n--> Valor invalido.")
                    continue
                cliente.realizar_transacao(conta, Saque(valor))

            case "e":
                cpf = input("CPF do cliente: ")
                cliente = filtrar_cliente(cpf, clientes)
                if not cliente:
                    print("\n--> Cliente nao encontrado.")
                    continue
                conta = recuperar_conta_cliente(cliente)
                if conta:
                    exibir_extrato(conta)

            case "nu":
                cpf = input("CPF (somente numeros): ")
                if filtrar_cliente(cpf, clientes):
                    print("\n--> Ja existe cliente com esse CPF.")
                    continue
                nome = input("Nome completo: ")
                nasc = input("Data de nascimento (dd-mm-aaaa): ")
                endereco = input("Endereco (logradouro, nro - bairro - cidade/sigla): ")
                clientes.append(Cliente(nome, nasc, cpf, endereco))
                print("\n--> Cliente criado com sucesso!")

            case "nc":
                cpf = input("CPF do cliente: ")
                cliente = filtrar_cliente(cpf, clientes)
                if not cliente:
                    print("\n--> Cliente nao encontrado.")
                    continue
                numero_conta = len(contas) + 1
                conta = ContaCorrente.nova_conta(cliente, numero_conta)
                cliente.adicionar_conta(conta)
                contas.append(conta)
                print("\n--> Conta criada com sucesso!")

            case "lc":
                listar_contas(contas)

            case "q":
                print("\n--> Saindo do sistema...")
                break

            case _:
                print("\n--> Opcao invalida.")


if __name__ == "__main__":
    main()
