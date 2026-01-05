class Balance:
    def __set_name__(self,owner,name):
        self.private_name = "_"+name
    def __get__(self,obj,owner):
        if obj is None:
            return self
        else:
            return getattr(obj, self.private_name)
    
    def __set__(self,obj,value):
        if not hasattr(obj, "_validate_balance"):
            raise AttributeError("_validate_balance must be implemented to set attribute")
        else:
            if(obj._validate_balance(value)):
                setattr(obj, self.private_name, value)
            else:
                raise ValueError("Invalid attribute value")
       
    
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
        
        acc1.withdraw(amount)
        acc2.deposit(amount)
        
       
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
            
        new_balance = self.balance - amount
        if(self._validate_balance(new_balance)):
            self.balance = new_balance
            self.transactions.append(f"Rs {amount} withdrawn")
        else:
            raise ValueError(f"Insufficient balance")
           

    def _validate_balance(self,value):
        if(value>=0):
            return True
        else: return False

   
    
class SavingsAccount(Account):
    interest_rate = 0.05 #5% interest rate
    acc_type = "SavingsAccount"

    def apply_interest(self):
        interest = self.balance*self.interest_rate
        self.balance+= interest
        self.transactions.append(f"Rs {interest} interest added")
        print(f"Rs {interest} interest added")

   

class CurrentAccount(Account):
    overdraft_limit = 50000
    acc_type = "CurrentAccount"

    def withdraw(self,amount):
        if(amount<=0):
            raise ValueError("Can't withdraw negative or zero amount")
        
        new_balance = self.balance- amount
        if(self._validate_balance(new_balance)):
            self.balance = new_balance
            self.transactions.append(f"Rs {amount} withdrawn")
        else: 
            raise ValueError(f"Overdraft limit is being crossed")
            
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
#account1.deposit(-2000)
account2.deposit(5000)
account1.deposit(2000)
account2.withdraw(2000)
account1.withdraw(3000)
account3.deposit(2000)
print(account1.balance, account2.balance)
#mybank.transfer(account1, account3,3000)
mybank.transfer(account3, account1,19000)
print(account1.balance, account3.balance)



    