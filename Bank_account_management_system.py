from datetime import datetime


class Transaction:
    def __init__(
        self,
        tx_type,
        amount,
        source_account=None,
        target_account=None,
        note=""
    ):
        self.tx_type = tx_type
        self.amount = amount
        self.source_account_number = source_account
        self.target_account_number = target_account
        self.note = note
        self.timestamp = datetime.now()

    def __repr__(self):
        return (
            f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"{self.tx_type} {self.note} | Rs {self.amount} |"
        )


class Balance:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if not hasattr(obj, "_validate_balance"):
            raise AttributeError("_validate_balance must be implemented to set attribute")
        if obj._validate_balance(value):
            setattr(obj, self.private_name, value)
        else:
            raise ValueError("Invalid attribute value")

    def __delete__(self, obj):
        raise AttributeError(f"{self.private_name} cannot be deleted")


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account):
        if account.acc_number in self.accounts:
            raise ValueError("Account already exists")
        self.accounts[account.acc_number] = account

    def get_account(self, account_number):
        if account_number not in self.accounts:
            raise ValueError("Account not found!")
        return self.accounts[account_number]

    def transfer(self, acc1, acc2, amount):
        if amount <= 0:
            raise ValueError("transfer amount must be positive")

        if (
            acc1.acc_number not in self.accounts
            or acc2.acc_number not in self.accounts
        ):
            raise ValueError("Invalid account/accounts")

        acc1.withdraw(amount)
        acc2.deposit(amount)

        acc1.transactions.append(
            Transaction(
                "Transfer_OUT",
                amount,
                target_account=acc2.acc_number
            )
        )
        acc2.transactions.append(
            Transaction(
                "Transfer_IN",
                amount,
                source_account=acc1.acc_number
            )
        )

    def show_account_summary(self, acc):
        print(
            f"Account number: {acc.acc_number}, "
            f"Account holder: {acc.name}, "
            f"Account type: {acc.acc_type}, "
            f"Current balance: {acc.balance} "
            f"Transaction History: {acc.transactions}"
        )


class Account:
    balance = Balance()
    acc_type = "GenericAccount"

    def __init__(self, acc_number, holder_name, acc_balance):
        self.acc_number = acc_number
        self.name = holder_name
        self.balance = acc_balance
        self.transactions = []
        self.withdraw_error_msg = "Insufficient balance"

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Can't deposit negative or zero amount")
        self.balance += amount
        self.transactions.append(Transaction("DEPOSIT", amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Can't withdraw negative or zero amount")

        new_balance = self.balance - amount
        try:
            self.balance = new_balance
            self.transactions.append(Transaction("WITHDRAW", amount))
        except ValueError:
            raise ValueError(self.withdraw_error_msg) from None

    def _validate_balance(self, value):
        return value >= 0


class SavingsAccount(Account):
    interest_rate = 0.05
    acc_type = "SavingsAccount"

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.transactions.append(
            Transaction("DEPOSIT", interest, note="Interest")
        )


class CurrentAccount(Account):
    overdraft_limit = 50000
    acc_type = "CurrentAccount"
    withdraw_error_msg = "Overdraft limit is being crossed"

    def _validate_balance(self, value):
        return value >= -self.overdraft_limit




    