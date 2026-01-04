class Balance:
    def __set_name__(self,owner,name):
        self.private_name = "_"+name
    def __get__(self,obj,owner):
        if obj is None:
            return self
        else:
            return getattr(obj, self.private_name)
    
    def __set__(self,obj,value):
        validator = hasattr(obj, "_validate_balance")
        if not validator:
            raise NotImplementedError("Account must implement _validate_balance")
        if (obj._validate_balance(value)):
            setattr(obj, self.private_name, value)
        else: raise ValueError("Invalid balance for account type")
    
    def __delete__(self,obj):
        raise AttributeError(f"{self.private_name} cannot be deleted")
class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account):
        self.accounts.update({account.acc_number: account})

    def find_account(self,account):
        if(account.acc_number in self.accounts):
            return True
        else:
            return False
    
    def transfer(self,acc1, acc2, amount):
        if(amount<=0):
            raise ValueError("transfer amount must be positive")
        
        if (acc1.acc_number not in self.accounts or acc2.acc_number not in self.accounts):
            raise ValueError("Invalid account/accounts")
        
        new_balance = acc2.balance+ amount
        if not acc2._validate_balance(new_balance):
            raise ValueError("Cannot deposit this amount in acc2")
        
        acc1.withdraw(amount)
        acc2.deposit(amount)
        print("Successfully transfered money")
        acc1.transactions.append(f"Transferred Rs {amount} to {acc2.acc_number}")
        acc2.transactions.append(f"Received Rs {amount} from {acc1.acc_number}")
    

       
    def show_account_summary(self, acc):
        print(f"Account number: {acc.acc_number}, Account holder: {acc.name}, Account type: {acc.acc_type}, Current balance: {acc.balance} Transaction History: {acc.transactions}")





class Account:
    balance = Balance()
    acc_type = "GenericAccount"
    def __init__(self,acc_number,holder_name,acc_balance):
        self.acc_number = acc_number
        self.name = holder_name
        self.balance = acc_balance
        self.transactions = [f"Account created with Rs {self.balance} "]

    def deposit(self,amount):
        if(amount<=0):
            raise ValueError("Can't deposit negative or zero amount")
            
        else:
            self.balance+= amount
            self.transactions.append((f"deposited Rs {amount}"))
    def withdraw(self, amount):
        if(amount<=0):
            raise ValueError("Can't withdraw negative or zero amount")
            
        if(amount> self.balance):
            raise ValueError("Transaction failed!! insufficient balance")
        else:
            self.balance-=amount
            self.transactions.append(f"Rs {amount} withdrawn")
   
    
class SavingsAccount(Account):
    interest_rate = 0.05 #5% interest rate
    acc_type = "SavingsAccount"

    def apply_interest(self):
        interest = self.balance*self.interest_rate
        self.balance+= interest
        self.transactions.append(f"Rs {interest} interest added")
        print(f"Rs {interest} interest added")

    def _validate_balance(self, value):
        if(value>=0):
            return True
        else: return False

class CurrentAccount(Account):
    overdraft_limit = 50000
    acc_type = "CurrentAccount"

    def withdraw(self,amount):
        if(amount<=0):
            raise ValueError("Can't withdraw negative or zero amount")
        
        if(self.overdraft_limit+self.balance>= amount):
            self.balance-= amount
            self.transactions.append(f"Rs {amount} withdrawn")
        else: 
            raise ValueError("Overdraft limit is being crossed")
            
    def _validate_balance(self,value):
        if(value>= -self.overdraft_limit):
            return True
        else: return False

    
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
print(mybank.find_account(account1))
print(mybank.find_account(account2))
print(account1.balance, account3.balance) # checking balance of account1 and account2 before making transaction
mybank.transfer(account3,account1, 6000)
mybank.transfer(account1,account3, 1000)
print(account1.balance)
account1.apply_interest()
print(account1.balance)
account3.withdraw(50000)
print(account3.balance)
mybank.show_account_summary(account1)


    