from datetime import datetime
from checkinator import *
from database import *

##  кошелек - основная логика взаимодействия с кошельком
class Wallet(ValueCheck):

    def __init__(self, balance=0, db_name='wallet'):
        self.db = Database(db_name + '.db')
        self.__balance = round(self.db.select_balance(), 2)

    def get_balance(self):
        return self.__balance


    def top_up(self, summa):
        if not self.is_summa_valid(summa):
            return (False, 'Incorrect sum. It must be a positive number. Please, try again.')

        self.__balance += round(float(summa), 2)
        self.db.save_balance(self.__balance, 'balance top up', datetime.today().strftime('%d.%m.%Y'))

        return (True, 'Done!')


    def update_balance_add(self, cost):
        self.__balance -= cost
        self.db.save_balance(self.__balance, 'expense add', datetime.today().strftime('%d.%m.%Y'))


    def update_balance_delete(self, cost):
        self.__balance += cost
        self.db.save_balance(self.__balance, 'expense delete', datetime.today().strftime('%d.%m.%Y'))


    def add_expenses(self, cost, date, name, category):
        if not self.is_cost_valid(cost):
            return (False, 'Invalid cost. Cost must be a non-negative number.')
        elif not self.is_date_valid(date):
            return (False, 'Invalid date. Date must be dd.mm.yyyy, not earlier than 1974 and not later than today.')
        elif not self.is_name_valid(name):
            return (False, "Invalid good's name. Good's name cannot be empty.")
        elif not self.is_length_valid(name):
            return (False, "Name cannot be longer than 100 letters.")
        elif not self.is_name_valid(category):
            return (False, 'Invalid category name. Category cannot be empty.')
        elif not self.is_length_valid(category):
            return (False, "Category name cannot be longer than 100 letters.")

        if date == 't':
            date = datetime.today().strftime('%d.%m.%Y')

        if not self.is_balance_valid(self.__balance - round(float(cost), 2)):
            return (False, 'Too expensive. It cannot be bought.')

        self.db.insert_expense(cost, date, name, category)
        self.update_balance_add(round(float(cost), 2))

        return (True, 'Expense was added to your list!')


    def delete_expense(self, cost, date, name, category):
        if not self.is_cost_valid(cost):
            return (False, 'Invalid cost. Cost must be a non-negative number.')
        elif not self.is_date_valid(date):
            return (False, 'Invalid date. Date must be dd.mm.yyyy, not earlier than 1974 and not later than today.')
        elif not self.is_name_valid(name):
            return (False, "Invalid good's name. Good's name cannot be empty.")
        elif not self.is_length_valid(name):
            return (False, "Name cannot be longer than 100 letters.")
        elif not self.is_name_valid(category):
            return (False, 'Invalid category name. Category cannot be empty.')
        elif not self.is_length_valid(category):
            return (False, "Category name cannot be longer than 100 letters.")

        if date == 't':
            date = datetime.today().strftime('%d.%m.%Y')

        expenses = self.db.select_expense(cost, date, name, category)
        if not expenses:
            return (False, 'There are no such expenses in your list.')

        self.db.delete_expense(cost, date, name, category)
        self.update_balance_delete(round(float(cost), 2) * len(expenses))

        return (True, 'Expense was deleted from your list!')


    def show_expenses_by_date(self, date):
        if not self.is_date_valid(date):
            return (False, 'Invalid date. Date must be dd.mm.yyyy, not earlier than 1974 and not later than today.')

        if date == 't':
            date = datetime.today().strftime('%d.%m.%Y')

        expenses = self.db.select_expenses_by_date(date)
        if not expenses:
            return (False, 'No expenses made on this date.')

        return (True, [i[1:] for i in expenses])


    def show_expenses_by_category(self, category):
        if not self.is_name_valid(category):
            return (False, 'Invalid category name. Category cannot be empty.')
        elif not self.is_length_valid(category):
            return (False, "Category name cannot be longer than 100 letters.")

        expenses = self.db.select_expenses_by_category(category)
        if not expenses:
            return (False, 'No expenses made in this category.')

        return (True, [i[1:] for i in expenses])

