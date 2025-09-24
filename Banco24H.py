class Conta:
    def __init__(self, agencia, numero_conta, senha, nome, cpf, saldo=0, limite=2000):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.senha = senha
        self.nome = nome
        self.cpf = cpf
        self.saldo = saldo
        self.chavePix = None
        self.bloqueada = False
        self.limite = limite
        self.extrato = []
        
    def autenticar(self, agencia_input, conta_input, senha_input):
        return (
            not self.bloqueada and
            self.agencia == agencia_input and
            self.numero_conta == conta_input and
            self.senha == senha_input
        )

    def mostrar_dados(self):
        print("\nDados da Conta")
        print(f"Titular: {self.nome}")
        print(f"CPF: {self.cpf}")
        print(f"Agência: {self.agencia}")
        print(f"Conta: {self.numero_conta}")
        print(f"Saldo: R$ {self.saldo:.2f}")
        print(f"Limite de crédito para relizar Pix: {self.limite:.2f}")
        
        if self.chavePix:
            print(f"Chave Pix cadastrada: {self.chavePix}")
        else:
            print("Chave Pix não cadastrada")
        print("\n")

    def cadastrar_chave_pix(self, chave):
        if self.chavePix:
            print(f"Já existe uma chave Pix cadastrada: {self.chavePix}")
            return
        chave = (chave or "").strip()
        if not chave:
            print("Chave Pix inválida")
            return
        self.chavePix = chave
        print(f"Chave Pix '{self.chavePix}' cadastrada com sucesso!")

    def realizar_pix(self, destinatario, valor):
        if not self.chavePix:
            print("Você não tem chave Pix cadastrada. Cadastre uma antes de enviar Pix.")
            return
        if not destinatario or not destinatario.chavePix:
            print("Destinatário inválido ou sem chave Pix cadastrada.")
            return
        if valor <= 0:
            print("Valor inválido.")
            return
        if valor > self.saldo + self.limite:
            print("Limite de crédito atingido.")
            return
        
        self.saldo -= valor
        destinatario.saldo += valor
        
        self.extrato.append(f"Pix enviado: -R$ {valor:.2f} para {destinatario.nome}")
        destinatario.extrato.append(f"Pix recebido: +R$ {valor:.2f} de {self.nome}")
        print(f"Pix de R$ {valor:.2f} enviado para {destinatario.nome} ({destinatario.chavePix}).")
        print(f"Seu novo saldo: R$ {self.saldo:.2f}")

    def alterar_senha(self):
        senha_atual = input("Digite sua senha atual: ")
        if senha_atual != self.senha:
            print("Senha atual incorreta. Não foi possível alterar a senha.")
            return
        nova_senha = input("Digite a nova senha: ")
        confirmar_senha = input("Confirme a nova senha: ")
        
        if nova_senha != confirmar_senha:
            print("As senhas não coincidem. Tente novamente.")
            return
        
        if not nova_senha:
            print("Senha não pode ser vazia.")
            return

        self.senha = nova_senha
        print("Senha alterada com sucesso!")

    def depositar(self, valor):
        if valor <= 0:
            print("Valor de depósito inválido.")
            return
        self.saldo += valor
        self.extrato.append(f"Depósito: +R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        print(f"Novo saldo: R$ {self.saldo:.2f}")

    def sacar(self, valor):
        if valor <= 0:
            print("Valor de saque inválido.")
            return
        if valor > self.saldo:
            print("Saldo insuficiente para saque.")
            return
        self.saldo -= valor
        self.extrato.append(f"Saque: -R$ {valor:.2f}")
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        print(f"Novo saldo: R$ {self.saldo:.2f}")
        
    def alterar_limite(self):
        try:
            novo_limite = float(input("Digite o novo limite de crédito: "))
            if novo_limite <= 0:
                print("O limite de crédito deve ser positivo.")
                return
            self.limite = novo_limite
            print(f"Novo limite de crédito definido: R$ {self.limite:.2f}")
        except ValueError:
            print("Valor inválido. Digite um número.")
            
    def mostrar_extrato(self):
        print("\nExtrato da Conta\n")
        if not self.extrato:
            print("Nenhuma movimentação registrada.")
        else:
            for movimento in self.extrato:
                print(movimento)
        print(f"Saldo atual: R$ {self.saldo:.2f}")

conta1 = Conta("1234", "56789-0", "1234", "Antonio Jr", 12345678901, saldo=0)
conta2 = Conta("1000", "10000-0", "1010", "Gabriel", 12345678902, saldo=0)

conta2.chavePix = "gabriel@gmail.com"

contas = [conta1, conta2]


def encontrar_conta_por_chave(chave):
    for conta in contas:
        if conta.chavePix == chave:
            return conta
    return None

tentativas = 0
max_tentativas = 3
conta_logada = None

while tentativas < max_tentativas and not conta_logada:
    print("\nAcesso ao Caixa Eletrônico")
    agencia_input = input("Digite o número da agência: ")
    conta_input = input("Digite o número da conta: ")
    senha_input = input("Digite sua senha: ")

    for conta in contas:
        if conta.autenticar(agencia_input, conta_input, senha_input):
            conta_logada = conta
            break

    if conta_logada:
        print(f"\nAcesso permitido! Bem-vindo, {conta_logada.nome}.")
        conta_logada.mostrar_dados()

        while True:
            print("\nMenu\n")
            print("1 - Cadastrar chave Pix")
            print("2 - Mostrar dados da conta")
            print("3 - Realizar Pix")
            print("4 - Alterar senha")
            print("5 - Depositar")
            print("6 - Sacar")
            print("7 - Alterar limite")
            print("8 - Mostra Extrato")
            print("9 - Sair\n")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                chave = input("Digite a chave Pix que deseja cadastrar: ")
                conta_logada.cadastrar_chave_pix(chave)

            elif opcao == "2":
                conta_logada.mostrar_dados()

            elif opcao == "3":
                chave_dest = input("Digite a chave Pix do destinatário: ")
                destinatario = encontrar_conta_por_chave(chave_dest)
                if destinatario:
                    valor = float(input("Digite o valor do Pix: R$ "))
                    conta_logada.realizar_pix(destinatario, valor)
                else:
                    print("Chave Pix não encontrada.")

            elif opcao == "4":
                conta_logada.alterar_senha()
                
            elif opcao == "5":
                valor = float(input("Digite o valor do depósito: R$ "))
                conta_logada.depositar(valor)
                
            elif opcao == "6":
                valor = float(input("Digite o valor do saque: R$ "))
                conta_logada.sacar(valor)
            
            elif opcao == "7":
                conta_logada.alterar_limite()
                
            elif opcao == "8":
                conta_logada.mostrar_extrato()
                
            elif opcao == "9":
                print("Saindo... Obrigado por usar nosso banco!")
                break
            else:
                print("Opção inválida. Tente novamente.")
    else:
        print("\nDados incorretos. Verifique sua agência, conta ou senha.")
        tentativas += 1

        if tentativas < max_tentativas:
            print(f"Tentativa {tentativas}/{max_tentativas}. Tente novamente.")
        else:
            print("\nNúmero máximo de tentativas atingido. Acesso bloqueado.")
