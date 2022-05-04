from dataclasses import dataclass
from datetime import date
import pickle

@dataclass
class Transaction:
    amount: float
    is_deposit: bool = False
    transaction_date: date = date.today()
    vendor: str = ""
    memo: str = ""
    
    def __post_init__(self):
        if self.is_deposit:
            self.amount = abs(self.amount)
        else:
            self.amount = -abs(self.amount)
    
    def __add__(self, other):
        return self.amount + other.amount

class Bucket:
    # _instances = {}

    def __init__(self, name: str, start_total: float = 0) -> None:
        self.name = name
        self.total = start_total
        self.transactions = []
        
        self.new_transaction(0, memo="INITIAL")
        print(f"{self.name} (starting balance ${self.get_balance()}")
        #Bucket._instances[self.name] = self
    
    # @classmethod
    # def get_bucket(cls, name: str):
    #     try:
    #         return cls._instances[name]
    #     except KeyError:
    #         print(f"No bucket found matching name {name}")
    
    # @classmethod
    # def save_all_buckets(cls, filename="bucketdata"):
    #     with open(filename, 'wb') as f:
    #         pickle.dump(cls._instances, f)
    
    def new_transaction(self, amount, is_deposit=False, transaction_date=date.today(), vendor="", memo=""):
        self.transactions.append(Transaction(amount, is_deposit, transaction_date, vendor, memo))
        print(f"New balance for {self.name}: ${self.get_balance}")
    
    def move_to(self, amount: float, to_bucket: str):
        move_amount(amount, to_bucket, self.name)
        print(f"Moved ${amount} to {to_bucket}.")
    
    def deposit(self, deposit_amount, origin="manual"):
        self.balance += deposit_amount
        self.balance = round(self.balance, 2)
        print(f"deposited ${deposit_amount} - new balance ${self.balance}")
        self.history.append((deposit_amount, origin))
    
    def withdraw(self, withdrawal_amount, destination="manual"):
        self.balance -= withdrawal_amount
        self.balance = round(self.balance, 2)
        print(f"withdrew ${withdrawal_amount} - new balance ${self.balance}")
        self.history.append((-withdrawal_amount, destination))
    
    def get_transaction_sum(self):
        return sum([t.amount for t in self.transactions])
    
    def get_balance(self):
        transaction_sum = self.get_transaction_sum()
        self.balance = self.total + transaction_sum
        return self.balance
    
    def reset(self):
        self.total = 0
        self.transactions = []

        

def move_amount(amount: float, to_bucket: str = None, from_bucket: str = None):
    if to_bucket == None and from_bucket == None:
        raise ValueError("to_bucket and from_bucket cannot both be None")
    # add to to_bucket
    Bucket.get_bucket(to_bucket).deposit(amount)
    # subtract from from_bucket
    Bucket.get_bucket(from_bucket).withdraw(amount)