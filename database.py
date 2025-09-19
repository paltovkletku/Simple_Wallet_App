import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='wallet.db'):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.create_table_expenses()
            self.create_table_balance()
        except sqlite3.Error:
            exit()
    def create_table_expenses(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                                    id INTEGER PRIMARY KEY,
                                    cost REAL,
                                    date VARCHAR(10),
                                    name VARCHAR(100),
                                    category VARCHAR(100)
                                )''')
            self.conn.commit()
        except sqlite3.Error:
            exit()


    def insert_expense(self, cost, date, name, category):
        try:
            self.cursor.execute('INSERT INTO expenses (cost, date, name, category) VALUES (?, ?, ?, ?)',
                                (cost, date, name, category))
            self.conn.commit()
        except sqlite3.Error:
            exit()


    def delete_expense(self, cost, date, name, category):
        try:
            self.cursor.execute('DELETE FROM expenses WHERE cost = ? AND date = ? AND name = ? AND category = ?',
                            (cost, date, name, category))
            self.conn.commit()
        except sqlite3.Error:
            exit()


    def select_expenses_by_date(self, date):
        try:
            self.cursor.execute('SELECT * FROM expenses WHERE date = ?', (date,))
            expenses = self.cursor.fetchall()
            return expenses
        except sqlite3.Error:
            exit()


    def select_expense(self, cost, date, name, category):
        try:
            self.cursor.execute('SELECT * FROM expenses WHERE cost = ? AND date = ? AND name = ? AND category = ?', (cost, date, name, category))
            expenses = self.cursor.fetchall()
            return expenses
        except sqlite3.Error:
            exit()


    def select_expenses_by_category(self, category):
        try:
            self.cursor.execute('SELECT * FROM expenses WHERE category = ?', (category,))
            expenses = self.cursor.fetchall()
            return expenses
        except sqlite3.Error:
            exit()


    def create_table_balance(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS balance (
                                            id INTEGER PRIMARY KEY,
                                            balance REAL,
                                            type VARCHAR(20),
                                            date VARCHAR(10)
                                        )''')
            is_balance = self.cursor.execute('SELECT * FROM balance').fetchone()

            if is_balance is None:
                self.cursor.execute('INSERT INTO balance (balance, type, date) VALUES (?, ?, ?)',
                                    (0, 'wallet created', datetime.today().strftime('%d.%m.%Y')))
            self.conn.commit()
        except sqlite3.Error:
            exit()


    def select_balance(self):
        try:
            self.cursor.execute('''SELECT * FROM balance ORDER BY id DESC LIMIT 1''')
            balance = self.cursor.fetchone()
            return balance[1]
        except sqlite3.Error:
            exit()

    def save_balance(self, balance, type, date):
        try:
            self.cursor.execute('INSERT INTO balance (balance, type, date) VALUES (?, ?, ?)',
                                (balance, type, date))
            self.conn.commit()
        except sqlite3.Error:
            exit()


    def close(self):
        try:
            self.conn.close()
        except sqlite3.Error:
            exit()




