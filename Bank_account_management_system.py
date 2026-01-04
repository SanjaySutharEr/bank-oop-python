class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account):
        self.accounts.update({account.acc_number: account})

    def find_account(self,acc_num):
        if(acc_num in self.accounts):
            return True
        else:
            return False
    
    def transfer(self,acc1, acc2, amount):
        allowed = False
        if(acc1.acc_number in self.accounts and acc2.acc_number in self.accounts):
            if(acc1.acc_type =="SavingsAccount"):
                allowed = amount<= acc1.get_balance()
            elif(acc1.acc_type== "CurrentAccount"):
                allowed = amount<=acc1.get_balance()+ acc1.overdraft_limit
            if allowed:
                acc1.withdraw(amount)
                acc2.deposit(amount)
                print("succesfully transfered money")
                print(f"Available balance in account {acc1.acc_number}: {acc1.get_balance()}")
                print(f"Available balance in account {acc2.acc_number}: {acc2.get_balance()}")
            else:
                print("Insufficient balance! Can't trasfer money")
        else:
            print("Invalid account/accounts")

    
    def show_account_summary(self, acc):
        print(f"Account number: {acc.acc_number}, Account holder: {acc.name}, Account type: {acc.acc_type}, Current balance: {acc.get_balance()}")





class Account:
    def __init__(self,acc_number,holder_name,balance):
        self.acc_number = acc_number
        self.name = holder_name
        self._balance = balance
        self.transactions = [f"deposited Rs {self._balance} "]

    def deposit(self,amount):
        if(amount>0):
            self._balance+= amount
            self.transactions.append((f"deposited Rs {amount}"))
    def withdraw(self, amount):
        if(amount>0):
            if(amount> self._balance):
                print("Transaction failed!! insufficient balance")
            else:
                self._balance-=amount
                self.transactions.append(f"Rs {amount} withdrawn")
    def get_balance(self):
        return self._balance
    
class SavingsAccount(Account):
    interest_rate = 0.05 #5% interest rate
    acc_type = "SavingsAccount"

    def apply_interest(self):
        interest = self.get_balance()*self.interest_rate
        self.deposit(interest)
        print(f"Rs {interest} interest added")

class CurrentAccount(Account):
    overdraft_limit = 50000
    acc_type = "CurrentAccount"

    def withdraw(self,amount):
        if(amount>0):
            if(abs(self.get_balance()-amount)>self.overdraft_limit):
                print("Overdraft limit crossed! couldn't make transaction")
            else:
                self._balance-= amount
                self.transactions.append(f"Rs {amount} withdrawn")

    
mybank = Bank()
account1 = SavingsAccount("1234", "david laid", 500)
mybank.create_account(account1)
account2 = SavingsAccount("2345", "john mehra", 2000)
mybank.create_account(account2)
account3 = CurrentAccount("5647", "sara ali", 2000)
mybank.create_account(account3)

account1.deposit(2000)
account1.deposit(-2000)
account2.deposit(5000)
account1.deposit(2000)
account2.withdraw(2000)
account1.withdraw(5000)
account3.deposit(2000)

print(mybank.accounts)
mybank.show_account_summary(account1)
print(mybank.find_account("1234"))
print(mybank.find_account("1111"))
print(account1.get_balance(), account3.get_balance()) # checking balance of account1 and account2 before making transaction
mybank.transfer(account3,account1, 6000)
mybank.transfer(account1,account3, 1000)
print(account1.get_balance())
account1.apply_interest()
print(account1.get_balance())
account3.withdraw(50000)
print(account3.get_balance())


    