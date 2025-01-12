import __init__
from views.view import SubscriptionService  # Corrigido o typo
from models.database import engine
from models.model import *
from datetime import datetime  # Importe datetime para usar strptime
from decimal import Decimal


class UI:
    def __init__(self):
        self.subscription_service = SubscriptionService(engine)

    def start(self):  # Método start dentro da classe
        while True:
            print(
                """
                1 - Cadastrar assinatura
                2 - Remover assinaturas cadastradas
                3 - Valor total de assinaturas
                4 - Pagar assinatura
                5 - Gastos dos últimos 12 meses
                6 - Sair
                """
            )

            option = input("Digite a opção desejada: ")

            if option == "1":
                self.add_subscription()
            elif option == "2":
                self.remove_subscription()  # Corrigido typo
            elif option == "3":
                self.total_value()
            elif option == "4":
                self.pay()
            elif option == "5":
                self.subscription_service.gen_chart()
            elif option == "6":  # Adicionado caso para sair
                break
            else:
                print(
                    "Opção inválida. Tente novamente."
                )  # Mensagem para opção inválida

    def add_subscription(self):
        name = input("Nome: ")
        site = input("Site: ")
        try:  # tratamento de erro para data
            data_assinatura = datetime.strptime(
                input("Data da assinatura (dd/mm/aaaa): "), "%d/%m/%Y"
            )  # Corrigido strptime
        except ValueError:
            print("Formato de data inválido. Use dd/mm/aaaa.")
            return  # Sai da função se a data for inválida
        try:  # tratamento de erro para valor
            value = Decimal(input("Valor: "))

        except InvalidOperation:
            print("Valor inválido. Digite um número decimal.")
            return  # Sai da função se o valor for inválido

        subscription = Subscription(
            empresa=name, site=site, data_assinatura=data_assinatura, valor=value
        )  # Corrigido varlor para valor
        self.subscription_service.create(subscription)  # Corrigido subcripiton_service
        print("Assinatura cadastrada com sucesso!")

    def remove_subscription(self):  # Corrigido typo
        subscriptions = self.subscription_service.list_all()
        if not subscriptions:  # verifica se tem assinaturas antes de tentar exibir
            print("Nenhuma assinatura cadastrada.")
            return  # Sai da função se não houver assinaturas
        print("Assinaturas cadastradas: ")
        for i in subscriptions:
            print(f"[{i.id}] -> {i.empresa}")
        try:  # tratamento de erro para input de id
            option = int(input("Escolha a assinatura que deseja remover: "))
            self.subscription_service.delete(option)
            print("Assinatura removida com sucesso!")
        except ValueError:
            print("Entrada inválida. Digite um número.")
        except Exception as e:  # tratamento de erro mais geral
            print(f"Erro ao remover assinatura: {e}")

    def total_value(self):
        print(
            f"O valor total de assinaturas é: R$ {self.subscription_service.total_value()}"
        )

    def pay(self):
        subscriptions = self.subscription_service.list_all()
        if not subscriptions:  # verifica se tem assinaturas antes de tentar exibir
            print("Nenhuma assinatura cadastrada.")
            return  # Sai da função se não houver assinaturas
        print("Assinaturas cadastradas: ")
        for i in subscriptions:
            print(f"[{i.id}] -> {i.empresa}")
        try:  # tratamento de erro para input de id
            option = int(input("Escolha a assinatura que deseja pagar: "))
            self.subscription_service.pay(option)
            print("Assinatura paga com sucesso!")
        except ValueError:
            print("Entrada inválida. Digite um número.")
        except Exception as e:  # tratamento de erro mais geral
            print(f"Erro ao pagar assinatura: {e}")


# Cria a instância da UI *fora* do loop
ui = UI()
ui.start()  # Chama o método start() na instância
