from heapq import heappop, heappush

class CashFlowMinimizer:
    def __init__(self, n):
        self.n = n  # Number of individuals
        self.net_balance = [0] * n  # Net balance for each individual

    def add_transaction(self, payer, payee, amount):
        self.net_balance[payer] -= amount
        self.net_balance[payee] += amount

    def minimize_cash_flow(self):
        creditors = []  # People who need to receive money
        debtors = []    # People who need to pay money

        for i in range(self.n):
            if self.net_balance[i] > 0:
                heappush(creditors, (-self.net_balance[i], i))
            elif self.net_balance[i] < 0:
                heappush(debtors, (self.net_balance[i], i))

        transactions = []

        while creditors and debtors:
            credit_amount, creditor = heappop(creditors)
            debt_amount, debtor = heappop(debtors)

            credit_amount = -credit_amount

            settlement_amount = min(credit_amount, -debt_amount)

            transactions.append((debtor, creditor, settlement_amount))

            credit_amount -= settlement_amount
            debt_amount += settlement_amount

            if credit_amount > 0:
                heappush(creditors, (-credit_amount, creditor))
            if debt_amount < 0:
                heappush(debtors, (debt_amount, debtor))

        return transactions

# Example Usage
if __name__ == "__main__":
    n = 3  # Number of people
    cfm = CashFlowMinimizer(n)

    # Add transactions: (payer, payee, amount)
    cfm.add_transaction(0, 1, 1500)
    cfm.add_transaction(1, 2, 2500)
    cfm.add_transaction(0, 2, 2000)

    # Minimize cash flow
    result = cfm.minimize_cash_flow()

    print("Optimized Transactions:")
    for debtor, creditor, amount in result:
        print(f"Person {debtor} pays Person {creditor}: {amount}")
