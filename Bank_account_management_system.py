from datetime import datetime
from enum import Enum, auto
class TransactionType(Enum):
    DEPOSIT = auto()
    WITHDRAW = auto()
    TRANSFER_IN = auto()
    TRANSFER_OUT= auto()
    INTEREST = auto()

class Transaction:
    def __init__(
            self,
            tx_type: TransactionType,
            amount,
            source_account=None,
            target_account=None,
            note=""
    ):
        if (not isinstance(amount,(int,float)) or amount<=0):
            raise ValueError("Invalid transaction amount!")
        if not isinstance(tx_type, TransactionType):
            raise TypeError(f"Expected a TransactionType enum member, got {type(tx_type)}")
        if((tx_type ==(TransactionType.DEPOSIT) or tx_type ==TransactionType.WITHDRAW or tx_type == TransactionType.INTEREST) and (source_account!=None or target_account!=None)):
            raise ValueError("Invalid transaction")
        if tx_type == TransactionType.TRANSFER_IN and source_account is None:
            raise ValueError("TRANSFER_IN requires source_account")

        if tx_type == TransactionType.TRANSFER_OUT and target_account is None:
            raise ValueError("TRANSFER_OUT requires target_account")

        super().__setattr__("tx_type", tx_type)
        super().__setattr__("amount", amount)
        super().__setattr__("source_account_number", source_account)
        super().__setattr__("target_account_number", target_account)
        super().__setattr__("note", note)
        super().__setattr__("timestamp", datetime.now())
       

    def __setattr__(self, attribute, value):
        if hasattr(self, attribute):
            raise AttributeError("Attribute cannot be modified")
        else: super().__setattr__(attribute,value)
        

    def __repr__(self):
        return (
            f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"{self.tx_type.name} {self.note} | Rs {self.amount} |"
        )
class Balance:
    def __set_name__(self,owner,name):
        self.private_name = "__"+name
    def __get__(self,obj,owner):
        if obj is None:
            return self
        else:
            if not hasattr(obj, self.private_name):
                raise AttributeError("balance hasn't been set yet")
            else:
                return getattr(obj, self.private_name) 
    
    def __set__(self,obj,value):
        if not hasattr(obj, self.private_name):
            if value < 0:
                raise ValueError("Account cannot be created with negative balance")
        if not isinstance(value, (int,float)):
            raise ValueError("Balance must be numeric")
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
        if(account.acc_number in self.accounts):
            raise ValueError("Account already exists")
        else:
            self.accounts.update({account.acc_number: account})

    def get_account(self,account_number):
        if(not account_number in self.accounts):
            raise ValueError("Account not found!")
        else: return self.accounts[account_number]
    
    def transfer(self,acc_number1, acc_number2, amount):
        if(not isinstance(amount,(int,float))):
            raise ValueError("transferring amount must be numeric")
        if(acc_number1==acc_number2):
            raise ValueError("Cannot transfer to same account")
        if(amount<=0):
            raise ValueError("transfer amount must be positive")
        
        if (acc_number1 not in self.accounts or acc_number2 not in self.accounts):
            raise ValueError("Invalid account/accounts")
        
        self.accounts[acc_number1].transfer_to(amount, acc_number2)
        self.accounts[acc_number2].transfer_from(amount, acc_number1)
        
       
    def show_account_summary(self, acc_number):
        if(acc_number in self.accounts):
            return {"Account Number": self.accounts[acc_number].acc_number,
                "Account Holder": self.accounts[acc_number].name,
                "Current Balance": self.accounts[acc_number].balance,
                "Last 10 transactions": self.accounts[acc_number].last_n_transactions(10)}





class Account:
    balance = Balance()
    acc_type = "GenericAccount"
    def __init__(self,acc_number,holder_name,acc_balance):
        self.acc_number = acc_number
        self.name = holder_name
        self.balance = acc_balance
        self.transactions = []
        self.withdraw_error_msg = "Insufficient balance"

    
    def deposit(self,amount):
        if(not isinstance(amount, (int,float))):
            raise ValueError("Depositing amount must be numeric")
        if(amount<=0):
            raise ValueError("Can't deposit negative or zero amount")
            
        else:
            self.balance+= amount
        self._record_transaction(TransactionType.DEPOSIT,amount)
        
        
        
    def withdraw(self, amount):
        if(not isinstance(amount, (int,float))):
            raise ValueError("Withdrawing amount must be numeric")
        if(amount<=0):
            raise ValueError("Can't withdraw negative or zero amount")
            
        new_balance = self.balance - amount
        try:
            self.balance = new_balance
        except ValueError:
            raise ValueError(self.withdraw_error_msg) from None
        self._record_transaction(TransactionType.WITHDRAW, amount)
        
    def transfer_from(self,amount,source_account):
        if(source_account== self.acc_number):
            raise ValueError("Can't transfer to account itself!")
        if(not isinstance(amount, (int,float))):
            raise ValueError("Transferring amount must be numeric!")
        if(amount<=0):
            raise ValueError("Can't transfer negative or zero amount!")
            
        else:
            self.balance+= amount
            self._record_transaction(TransactionType.TRANSFER_IN, amount,source_account= source_account)

    def transfer_to(self, amount, target_account):
        if(not isinstance(amount, (int,float))):
            raise ValueError("Transferring amount must be numeric")
        if(amount<=0):
            raise ValueError("Can't transfer negative or zero amount")
            
        new_balance = self.balance - amount
        try:
            self.balance = new_balance
        except ValueError:
            raise ValueError("Transfer failed! Transferring amount is exceeding overdraft_limit") from None
        self._record_transaction(TransactionType.TRANSFER_OUT,amount,target_account=target_account)
        
        
    
           
           

    def _validate_balance(self,value):
        if(value>=0):
            return True
        else: return False

    def last_n_transactions(self,n):
        lasttransactions = []
        if len(self.transactions)<n:
            n = len(self.transactions)
        for i in range(1,n+1):
            lasttransactions.append(self.transactions[-i])
        lasttransactions.reverse()
        return lasttransactions
    
    def _record_transaction(self,tx_type, amount,source_account = None, target_account = None, note = ""):
        tx = Transaction(tx_type,amount, source_account = source_account, target_account = target_account, note=note)
        self.transactions.append(tx)
        


       

   
    
class SavingsAccount(Account):
    interest_rate = 0.05 #5% interest rate
    acc_type = "SavingsAccount"

    def apply_interest(self):
        interest = self.balance*self.interest_rate
        self.balance+= interest
        self._record_transaction(TransactionType.INTEREST,interest)
       

   

class CurrentAccount(Account):
    overdraft_limit = 50000
    acc_type = "CurrentAccount"
    withdraw_error_msg = "Overdraft limit is being crossed"

            
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
mybank.transfer(account1.acc_number, account3.acc_number,1000)
#mybank.transfer(account3, account1,19000)
print(account1.balance, account3.balance)
# account1.apply_interest()
print(account1.transactions)
print(account1.last_n_transactions(3))
#print(mybank.show_account_summary("1234"))


    