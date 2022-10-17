from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self.saldo

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

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
        saldo = self.saldo

        if valor > saldo:
            print("\n Erro, Saldo Insuficiente!!") 
        elif(valor > 0):
            self._saldo -= valor
            print("\n Saque realizado com sucesso!")
            return True
        else:
            print("\nErro: O valor informado é inválido")
        return False

    def depositar_conta(self, valor):
        print("=>>>>>>>>>>>> parou")
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
        else:
            print("Erro: O valor digitado é inválido!")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes 
                            if transacao["tipo"] == Saque.__name__])

        if (valor > self.limite):
            print("\nErro: O valor do saque excedeu o limite!")

        elif (numero_saques >= self.limite_saques):
            print("Erro: Limite diario de saques atingido!")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agencia:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self) -> None:
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({"tipo": transacao.__class__.__name__, "valor": transacao.valor, "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")})

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        #print(conta.index)
        print(self.valor)
        print(conta.depositar_conta(self.valor))
        
        #sucesso_transacao = conta.depositar_conta(self.valor)
        #if sucesso_transacao:
        #   conta.historico.adicionar_transacao(self)

def menu():
    menu = """
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tCadastrar Novo Cliente
    [5]\tCadastrar Nova Conta
    [6]\tExibir Contas
    [7]\tSair
    """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Erro, o cliente não possui conta!")
        return
    # fixme: não permite cliente escolher a conta    
    return cliente.contas

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    

def sacar(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n*************> Extrato <*************")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
            print("****************************")

def cadastrar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Não existe cliente com este CPF!")
        return
    
    nome = input("Informe o nome: ")
    data_nascimento = input("Informe a data de nascimento: ")
    endereco = input("informe o endereço: ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n Cliente Cadastrado com sucesso!")

def cadastrar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente!")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    conta = ContaCorrente.nova_conta(cliente="cliente", numero="numero_conta")
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n>>>>> Conta Criada")

def listar_contas(contas):
    for conta in contas:
        print("=" + 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)
        
        elif opcao == "3":
            exibir_extrato(clientes)
        
        elif opcao == "4":
            cadastrar_cliente(clientes)
        
        elif opcao == "5":
            numero_conta = len(contas) + 1
            cadastrar_conta(numero_conta, clientes, contas)
        
        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            break

        else:
            print("Erro: Opção Inválida!")

main()