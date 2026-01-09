from datetime import datetime
from enum import Enum, auto
from dataclasses import dataclass,field
from decimal import Decimal, ROUND_HALF_UP



class AccountType(Enum):
    GENERICACCOUNT=auto()
    SAVINGSACCOUNT=auto()
    CURRENTACCOUNT=auto()



class TransactionType(Enum):
    DEPOSIT = auto()
    WITHDRAW = auto()
    TRANSFER= auto()
    INTEREST = auto()




@dataclass(frozen =True, slots = True)
class Transaction:

    tx_type: TransactionType
    amount: Decimal
    source_account:int=None
    target_account:int=None
    note: str =""
    timestamp: str = field(init =False)

    def __post_init__(self):
        object.__setattr__(self,"timestamp",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if(self.amount<0):
            raise ValueError("Invalid transaction amount")
        if not isinstance(self.tx_type, TransactionType):
            raise TypeError(f"Invalid transaction type! expected TransactionType got {type(self.tx_type)}")
        if(self.tx_type==TransactionType.DEPOSIT):
            if(self.source_account is None and self.target_account is not None):
                pass
            else:
                raise ValueError("Source account must be None and target account must be present for transaction type DEPOSIT")
        if(self.tx_type==TransactionType.WITHDRAW):
            if(self.source_account is not None and self.target_account is None):
                pass
            else:
                raise ValueError("Source account must be present and target account must be None for transaction type WITHDRAW")
        if(self.tx_type==TransactionType.INTEREST):
            if(self.source_account is None and self.target_account is not None):
                pass
            else:
                raise ValueError("Source account must be None and target account must be present for transaction type INTEREST")
           
        if(self.tx_type== TransactionType.TRANSFER):
            if(self.target_account is not None and self.source_account is not None):
                pass
            else:
                raise ValueError("Invalid Transaction! source account and target account both must be present for transaction type TRANSFER")
       
    
    def __repr__(self):
        base = f"[{self.timestamp}] {self.tx_type.name}: Rs {Decimal(str(self.amount))}"
        if self.source_account and self.target_account:
            return f"{base} ({self.source_account} -> {self.target_account})"
        return base

    
        


class Balance:
    def __set_name__(self,owner,name):
        self.name = "_"+name
    def __get__(self,obj,owner):
        if obj is None:
            return self
        else:
             return getattr(obj,self.name)
           
    def __set__(self,obj,value):
        raise AttributeError(f"Balance cannot be set directly")
       
       
    def __delete__(self,obj):
        raise AttributeError(f"{self.name} cannot be deleted")
    







class Bank:
    def __init__(self):
        self.accounts = {}
        self.transactions = []

    def create_account(self,acc_type,acc_number, acc_holder,acc_balance):
        if( not isinstance(acc_type,AccountType)):
            raise TypeError("Invalid account type!")
        if(acc_number in self.accounts):
            raise ValueError("Account already exists")
        else:
            if acc_type== AccountType.GENERICACCOUNT:
                account = Account(self, acc_number, acc_holder, acc_balance)
            if acc_type== AccountType.SAVINGSACCOUNT:
                account = SavingsAccount(self, acc_number, acc_holder, acc_balance)
            if acc_type== AccountType.CURRENTACCOUNT:
                account = CurrentAccount(self, acc_number, acc_holder, acc_balance)
            
            self.accounts.update({acc_number: account})

    def get_account(self,account_number):
        if(not account_number in self.accounts):
            raise ValueError("Account not found!")
        else: return self.accounts[account_number]
    
    def transfer(self,acc_number1, acc_number2, amount):
        amount = Decimal(str(amount))
        if (acc_number1 not in self.accounts or acc_number2 not in self.accounts):
            raise ValueError("Invalid account/accounts")
        if(self.accounts[acc_number1].can_withdraw(amount) and self.accounts[acc_number2].can_deposit(amount)):
            self._record_transaction(TransactionType.TRANSFER, amount, source_account= acc_number1, target_account= acc_number2)
            
        
    def _record_transaction(self,tx_type, amount,source_account = None, target_account = None, note = ""):
        tx = Transaction(tx_type,Decimal(str(amount)), source_account = source_account, target_account = target_account, note=note)
        self.transactions.append(tx)   
       
    def show_account_summary(self, acc_number):
        if(acc_number in self.accounts):
            return f"""
                Account Number": {self.accounts[acc_number].acc_number},
                Date of Creation: {self.accounts[acc_number].date_of_creation},
                Account Holder": {self.accounts[acc_number].name},
                Current Balance": {self.accounts[acc_number].current_balance()},
                Last 10 transactions": {self.accounts[acc_number].last_n_transactions(10)}
                                                                                          """
    
    def transactions_of_account(self,acc_number):
        transaction_list = [x for x in self.transactions if (x.source_account== acc_number or x.target_account==acc_number)]
        return transaction_list









class Account:
    starting_balance = Balance()
    acc_type = "GenericAccount"
    max_limit =Decimal("INFINITY")
    min_limit = Decimal("0.00")
    def __init__(self,bank,acc_number,holder_name,acc_balance):
        self.date_of_creation = datetime.now().strftime("%Y-%m-%d")
        self.bank = bank
        self.acc_number = acc_number
        self.name = holder_name
        self.__dict__["_starting_balance"]= Decimal(str(acc_balance))
        self.withdraw_error_msg = " Transaction Failed! Insufficient balance in account"
        self.deposit_error_msg = ""
        

    def current_balance(self):
        current_balance=Decimal(str(self.starting_balance))
        account_transactions=self.bank.transactions_of_account(self.acc_number)
        for trnstn in account_transactions:
            if(trnstn.source_account==self.acc_number):
                x=-1
            elif(trnstn.target_account==self.acc_number):
                x=1
            factor_mapping={"DEPOSIT": 1, "WITHDRAW": -1,"INTEREST":1, "TRANSFER": x}
            current_balance+= factor_mapping[trnstn.tx_type.name]*trnstn.amount
        return current_balance.quantize(Decimal("0.01"), rounding = ROUND_HALF_UP)


    
    def deposit(self,amount):
        amount=Decimal(str(amount))
        if self.can_deposit(amount):
            self.bank._record_transaction(TransactionType.DEPOSIT,amount,target_account=self.acc_number)
        else:
            raise ValueError(f"{self.deposit_error_msg}: {self.acc_number}")
        
        
        
    def withdraw(self, amount):
        amount=Decimal(str(amount))
        if self.can_withdraw(amount):
            self.bank._record_transaction(TransactionType.WITHDRAW, amount, source_account = self.acc_number)
        else:
            raise ValueError(f"{self.withdraw_error_msg}:{self.acc_number}")
        
    
        
        
    def can_deposit(self, amount):

        if(not isinstance(amount, (int,float,Decimal))):
            raise ValueError("Invalid Request! Amount must be numeric")
        amount = Decimal(str(amount))
        if(amount<=0):
            raise ValueError("Invalid request! Amount must be positive")
        new_balance = self.current_balance() + amount
        if(new_balance<=self.max_limit):
            return True
        else: return False

    def can_withdraw(self,amount):
        
        if(not isinstance(amount, (int,float,Decimal))):
            raise ValueError("Invalid Request! Amount must be numeric")
        amount=Decimal(str(amount))
        if(amount<=0):
            raise ValueError("Invalid Request! Amount must be positive")
            
        new_balance = self.current_balance() - amount
        if(new_balance>=self.min_limit):
            return True
        else: return False
           

    def last_n_transactions(self,n):
        full_list=self.bank.transactions_of_account(self.acc_number)
        return full_list[-n:][::-1]
    
        
    def __repr__(self):
        return f"Account No.: {self.acc_number}, Account Holder: {self.name}, Date of Creation: {self.date_of_creation}"

       

   
    
class SavingsAccount(Account):
    interest_rate = Decimal("0.05") #5% interest rate
    acc_type = "SavingsAccount"

    def apply_interest(self):
        interest = (self.current_balance()*self.interest_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.bank._record_transaction(TransactionType.INTEREST,interest, target_account = self.acc_number)
       

   

class CurrentAccount(Account):
    overdraft_limit = Decimal("50000.00")
    min_limit = -overdraft_limit
    acc_type = "CurrentAccount"
    withdraw_error_msg = "Overdraft limit is being crossed in Account"

            

    
mybank = Bank()
mybank.create_account(AccountType.CURRENTACCOUNT, "4674", "krish", 2000)

mybank.create_account(AccountType.SAVINGSACCOUNT,"2345", "john mehra", 2000)

mybank.create_account(AccountType.CURRENTACCOUNT,"5647", "sara ali", 2000)

mybank.accounts["4674"].deposit(400)
mybank.transfer("4674","2345", 1550)
print(mybank.get_account("4674"))
print(mybank.transactions_of_account("4674"))
print(mybank.get_account("4674").last_n_transactions(4))


    