import sqlite3
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from wallet import *


#  интерфейсный класс

class MyWalletAppGUI:
    def __init__(self, name='wallet'):
        self.my_wallet = Wallet(db_name = name)

        self.win = tk.Tk()
        self.win.config(bg='pink')
        self.win.title('MyWalletApp')
        self.win.geometry('500x650')
        self.win.resizable(False, False)

        self.menu_bar = tk.Menu(self.win)
        self.win.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.file_menu)
        self.file_menu.add_command(label="Exit app", command=self.exit_app)

        self.label = tk.Label(self.win, text="Welcome to MyWalletApp\nWhat do you want to do?", font=("Arial", 18),
                              pady=20)
        self.label.config(bg='pink')
        self.label.pack()

        self.button_frame = tk.Frame(self.win)
        self.button_frame.config(bg='pink')
        self.button_frame.pack(pady=10)

        self.top_up_button = tk.Button(self.button_frame, text="Top up balance", font=("Arial", 14), height=2,
                                       width=25, command=self.top_up_balance)
        self.top_up_button.grid(row=0, column=0, padx=10, pady=10)

        self.balance_button = tk.Button(self.button_frame, text="Show balance", font=("Arial", 14), height=2,
                                        width=25, command=self.show_balance)
        self.balance_button.grid(row=1, column=0, padx=10, pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add an expense", font=("Arial", 14), height=2,
                                    width=25, command=self.add_expense)
        self.add_button.grid(row=2, column=0, padx=10, pady=10)

        self.delete_button = tk.Button(self.button_frame, text="Delete an expense", font=("Arial", 14), height=2,
                                       width=25, command=self.delete_expense)
        self.delete_button.grid(row=3, column=0, padx=10, pady=10)

        self.show_by_date_button = tk.Button(self.button_frame, text="Show expenses by date", font=("Arial", 14),
                                             height=2, width=25, command=self.show_by_date)
        self.show_by_date_button.grid(row=4, column=0, padx=10, pady=10)

        self.show_by_category_button = tk.Button(self.button_frame, text="Show expenses by category",
                                                 font=("Arial", 14), height=2, width=25,
                                                 command=self.show_by_category)
        self.show_by_category_button.grid(row=5, column=0, padx=10, pady=10)



    def exit_app(self):
        self.my_wallet.db.close()
        self.win.quit()

    def top_up_balance(self):
        top_up_win = tk.Toplevel(self.win)
        top_up_win.config(bg='pink')
        top_up_win.title("Balance top up")
        top_up_win.geometry("300x200")

        amount_label = tk.Label(top_up_win, text="Enter sum:", font=('Arial', 12), bg='pink')
        amount_label.pack(pady=15)
        amount_entry = tk.Entry(top_up_win)
        amount_entry.pack()

        def top_up_amount():
            top_up_try = self.my_wallet.top_up(amount_entry.get())
            if not top_up_try[0]:

                messagebox.showerror("Error", top_up_try[1])
                amount_entry.delete(0, tk.END)

            else:
                messagebox.showinfo("Success", top_up_try[1])
                top_up_win.destroy()

        confirm_button = tk.Button(top_up_win, text="Top up!", font=('Arial', 12), height=1, width=12, command=top_up_amount)
        confirm_button.pack(side='bottom', pady=20)


    def show_balance(self):
        balance_win = tk.Toplevel(self.win)
        balance_win.config(bg='pink')
        balance_win.title("MyBalance")
        balance_win.geometry("300x200")
        balance_win.resizable(False, False)

        balance_text_label = tk.Label(balance_win, text="Your balance is: ", font=("Arial", 16), bg='pink')
        balance_text_label.pack(pady=15)

        balance = str(self.my_wallet.get_balance())
        balance_label = tk.Label(balance_win, text=balance, font=("Arial", 28), bg='pink')
        balance_label.pack()

        def close_balance_win():
            balance_win.destroy()

        confirm_button = tk.Button(balance_win, text="Done!", font=("Arial", 16), width=8, height=2, command=close_balance_win)
        confirm_button.pack(side='bottom', pady=30)


    def add_expense(self):
        add_expense_win = tk.Toplevel(self.win)
        add_expense_win.config(bg='pink')
        add_expense_win.title("Add an expense")
        add_expense_win.geometry("500x300")
        add_expense_win.resizable(False, False)

        cost_label = tk.Label(add_expense_win, text="Enter cost:", font=('Arial', 12), bg='pink')
        cost_label.pack(pady=3)
        cost_entry = tk.Entry(add_expense_win)
        cost_entry.pack(pady=2)

        date_label = tk.Label(add_expense_win, text="Enter date (dd.mm.yyyy; if it's today enter 't'):", font=('Arial', 12), bg='pink')
        date_label.pack(pady=3)
        date_entry = tk.Entry(add_expense_win)
        date_entry.pack(pady=2)

        name_label = tk.Label(add_expense_win, text="Enter good's name:", font=('Arial', 12), bg='pink')
        name_label.pack(pady=3)
        name_entry = tk.Entry(add_expense_win)
        name_entry.pack(pady=2)

        category_label = tk.Label(add_expense_win, text="Enter category name:", font=('Arial', 12), bg='pink')
        category_label.pack(pady=3)
        category_entry = tk.Entry(add_expense_win)
        category_entry.pack(pady=2)

        def add_expense():
            add_expense_try = self.my_wallet.add_expenses(cost_entry.get(), date_entry.get().lower(), name_entry.get().lower(), category_entry.get().lower())


            if not add_expense_try[0]:

                messagebox.showerror("Error", add_expense_try[1])
                cost_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
                category_entry.delete(0, tk.END)

            else:
                messagebox.showinfo("Success", add_expense_try[1])
                add_expense_win.destroy()

        confirm_button = tk.Button(add_expense_win, text="Add an expense", font=('Arial', 12), width=14, height=1, command=add_expense)
        confirm_button.pack(side='bottom', pady=20)


    def delete_expense(self):
        delete_expense_win = tk.Toplevel(self.win)
        delete_expense_win.config(bg='pink')
        delete_expense_win.title("Delete an expense")
        delete_expense_win.geometry("500x300")

        cost_label = tk.Label(delete_expense_win, text="Enter cost:", font=('Arial', 12), bg='pink')
        cost_label.pack(pady=3)
        cost_entry = tk.Entry(delete_expense_win)
        cost_entry.pack(pady=2)

        date_label = tk.Label(delete_expense_win, text="Enter date (dd.mm.yyyy; if it's today enter 't'):", font=('Arial', 12), bg='pink')
        date_label.pack(pady=3)
        date_entry = tk.Entry(delete_expense_win)
        date_entry.pack(pady=2)

        name_label = tk.Label(delete_expense_win, text="Enter good's name:", font=('Arial', 12), bg='pink')
        name_label.pack(pady=3)
        name_entry = tk.Entry(delete_expense_win)
        name_entry.pack(pady=2)

        category_label = tk.Label(delete_expense_win, text="Enter category name:", font=('Arial', 12), bg='pink')
        category_label.pack(pady=3)
        category_entry = tk.Entry(delete_expense_win)
        category_entry.pack(pady=2)

        def delete_expense():
            delete_expense_try = self.my_wallet.delete_expense(cost_entry.get(), date_entry.get().lower(), name_entry.get().lower(), category_entry.get().lower())

            if not delete_expense_try[0]:

                messagebox.showerror("Error", delete_expense_try[1])
                cost_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
                category_entry.delete(0, tk.END)

            else:
                messagebox.showinfo("Success", delete_expense_try[1])
                delete_expense_win.destroy()

        confirm_button = tk.Button(delete_expense_win, text="Delete an expense", font=('Arial', 12), width=14, height=1, command=delete_expense)
        confirm_button.pack(side='bottom', pady=20)


    def show_by_date(self):
        show_by_date_win = tk.Toplevel(self.win)
        show_by_date_win.config(bg='pink')
        show_by_date_win.title("Show expenses by date")
        show_by_date_win.geometry("975x450")

        date_label = tk.Label(show_by_date_win, text="Enter date (if it's today enter 't'):", font=('Arial', 12), bg='pink')
        date_label.pack(pady=5)
        date_entry = tk.Entry(show_by_date_win)
        date_entry.pack(pady=5)

        tree = ttk.Treeview(show_by_date_win, column=("c1", "c2", "c3", "c4"), show='headings')
        tree.column("#1", anchor=tk.CENTER)
        tree.heading("#1", text="COST")
        tree.column("#2", anchor=tk.CENTER)
        tree.heading("#2", text="DATE")
        tree.column("#3", anchor=tk.CENTER)
        tree.heading("#3", text="NAME")
        tree.column("#4", anchor=tk.CENTER)
        tree.heading("#4", text="CATEGORY")

        scrollbar = ttk.Scrollbar(show_by_date_win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(pady=5)

        sum_label = tk.Label(show_by_date_win, text=f"Total sum:", font=('Arial', 16), bg='pink')
        sum_label.pack(pady=5)

        def show_by_date():
            show_by_date_try = self.my_wallet.show_expenses_by_date(date_entry.get().lower())

            if not show_by_date_try[0]:

                messagebox.showerror("Error", show_by_date_try[1])
                date_entry.delete(0, tk.END)
                tree.delete(*tree.get_children())
                sum_label.config(text=f"Total sum:")


            else:
                summa = sum([round(float(i[0]), 2) for i in show_by_date_try[1]])
                tree.delete(*tree.get_children())

                for expense in show_by_date_try[1]:
                    tree.insert("", tk.END, values=expense)

                sum_label.config(text=f"Total sum: {summa}")

        def close_win():
            show_by_date_win.destroy()


        show_button = tk.Button(show_by_date_win, text="Show!", font=('Arial', 12), width=14, height=1, command=show_by_date)
        show_button.pack(pady=3)

        confirm_button = tk.Button(show_by_date_win, text='Done!', font=('Arial', 12), width=14, height=1, command=close_win)
        confirm_button.pack(pady=3)




    def show_by_category(self):
        show_by_category_win = tk.Toplevel(self.win)
        show_by_category_win.config(bg='pink')
        show_by_category_win.title("Show expenses by category")
        show_by_category_win.geometry("975x450")

        category_label = tk.Label(show_by_category_win, text="Enter category name:", font=('Arial', 12), bg='pink')
        category_label.pack(pady=5)
        category_entry = tk.Entry(show_by_category_win)
        category_entry.pack(pady=5)

        tree = ttk.Treeview(show_by_category_win, column=("c1", "c2", "c3", "c4"), show='headings')
        tree.column("#1", anchor=tk.CENTER)
        tree.heading("#1", text="COST")
        tree.column("#2", anchor=tk.CENTER)
        tree.heading("#2", text="DATE")
        tree.column("#3", anchor=tk.CENTER)
        tree.heading("#3", text="NAME")
        tree.column("#4", anchor=tk.CENTER)
        tree.heading("#4", text="CATEGORY")

        scrollbar = ttk.Scrollbar(show_by_category_win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(pady=5)
        sum_label = tk.Label(show_by_category_win, text=f"Total sum:", font=('Arial', 16), bg='pink')
        sum_label.pack(pady=5)

        def show_by_category():
            show_by_category_try = self.my_wallet.show_expenses_by_category(category_entry.get().lower())


            if not show_by_category_try[0]:

                messagebox.showerror("Error", show_by_category_try[1])
                category_entry.delete(0, tk.END)
                tree.delete(*tree.get_children())
                sum_label.config(text=f"Total sum:")



            else:
                tree.delete(*tree.get_children())
                summa = sum([round(float(i[0]), 2) for i in show_by_category_try[1]])

                for expense in show_by_category_try[1]:
                    tree.insert("", tk.END, values=expense)

                sum_label.config(text=f"Total sum: {summa}")




        def close_win():
            show_by_category_win.destroy()

        show_button = tk.Button(show_by_category_win, text="Show!", font=('Arial', 12), width=14, height=1, command=show_by_category)
        show_button.pack(pady=3)

        confirm_button = tk.Button(show_by_category_win, text='Done!', font=('Arial', 12), width=14, height=1, command=close_win)
        confirm_button.pack(pady=3)

    def run(self):
        self.win.mainloop()
