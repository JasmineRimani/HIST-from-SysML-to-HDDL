# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:47:21 2021

@author: jasmi
"""

class BankAccount():
    
    def __init__(self, deposit):
        self.amount = deposit

    def withdraw(self, amount):
        self.amount -= amount

    def deposit(self, amount):
        self.amount += amount

    def balance(self):
        return self.amount

# Let me create an instance of 'BankAccount' class with the initial
# balance as $2000.
myAccount = BankAccount(2000)

# Let me check if the balance is right.
print(myAccount.balance())

# Let me deposit my salary
myAccount.deposit(10000)

# Let me withdraw some money to buy dinner.
myAccount.withdraw(15)

# What's the balance left?
print( myAccount.balance())