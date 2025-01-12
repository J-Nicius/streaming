import __init__
from models.database import engine
from models.model import Subscription, Paymentes
from sqlmodel import *
from datetime import date, datetime


class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine

    def create(self, subscription: Subscription):
        with Session(self.engine) as session:
            session.add(subscription)
            session.commit()
            return subscription

    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            result = session.exec(statement).one()
            session.delete(result)
            session.commit()

    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
            return results

    def _has_pay(self, results):
        for result in results:
            print(result.date)
            if result.date.month == date.today().month:
                return True
        return False

    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = (
                select(Paymentes)
                .join(Subscription)
                .where(Subscription.empresa == subscription.empresa)
            )
            results = session.exec(statement).all()

            if self._has_pay(results):
                question = input("Conta paga, deseja paga novamente? Y ou N: ")

                if not question.upper() == "Y":
                    return

    def total_value(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()

        total = 0
        for result in results:
            total += result.valor
        return float(total)

    def _get_last_12_months_native(self):
        today = datetime.now()
        year = today.year
        month = today.month
        last_12_months = []
        for _ in range(12):
            last_12_months.append((year, month))
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        return last_12_months[::-1]

    def _get_value_for_month(self, last_12_months):
        with Session(self.engine) as session:
            statement = select(Paymentes)
            results = session.exec(statement).all()
            value_for_month = []
            for i in last_12_months:
                value = 0
                for result in results:
                    if result.date.month == i[1] and result.date.year == i[0]:
                        Value += float(result.subscription.valor)
                value_for_month.append(value)
            return value_for_month

    def gen_chart(self):
        last_12_months = self._get_last_12_months_native()
        value_for_month = self._get_value_for_month(last_12_months)
        last_12_months = list(map(lambda x: f"{x[0]}-{x[1]}", last_12_months))

        import matplotlib.pyplot as plt

        plt.plot(last_12_months, value_for_month)
        plt.show()
