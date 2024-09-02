import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd


class PersonalFinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance App")
        self.root.geometry("800x600")

        # Load and set background image
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Replace 'background.jpg' with your actual image path
        self.bg_image = Image.open("background.jpg")  
        self.bg_image = self.bg_image.resize((800, 600), Image.ANTIALIAS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Create a frame over the background
        self.frame = tk.Frame(self.canvas, bg="white", bd=2, relief=tk.RAISED)
        self.canvas.create_window(400, 300, window=self.frame)

        # Setup tabs
        self.tab_control = ttk.Notebook(self.frame)
        self.income_expense_tab = ttk.Frame(self.tab_control)
        self.tax_tab = ttk.Frame(self.tab_control)
        self.investment_tab = ttk.Frame(self.tab_control)
        self.budget_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.income_expense_tab, text='Income & Expenses')
        self.tab_control.add(self.tax_tab, text='Tax Calculator')
        self.tab_control.add(self.investment_tab, text='Investments')
        self.tab_control.add(self.budget_tab, text='Budget Planner')
        self.tab_control.pack(expand=1, fill='both')

        self.income_data = pd.DataFrame(columns=['Source', 'Amount'])
        self.expense_data = pd.DataFrame(columns=['Source', 'Amount'])
        self.investment_data = pd.DataFrame(columns=['Type', 'Amount'])

        self.create_income_expense_tab()
        self.create_tax_tab()
        self.create_investment_tab()
        self.create_budget_tab()

    def create_income_expense_tab(self):
        font_style = ("Arial", 14)

        # Labels and Entries for Income
        tk.Label(self.income_expense_tab, text="Income Source", font=font_style).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.income_expense_tab, text="Amount", font=font_style).grid(row=0, column=1, padx=10, pady=10)
        self.income_source = tk.Entry(self.income_expense_tab, font=font_style)
        self.income_amount = tk.Entry(self.income_expense_tab, font=font_style)
        self.income_source.grid(row=1, column=0, padx=10, pady=10)
        self.income_amount.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.income_expense_tab, text="Add Income", font=font_style, command=self.add_income).grid(row=1, column=2, padx=10, pady=10)

        # Labels and Entries for Expense
        tk.Label(self.income_expense_tab, text="Expense Source", font=font_style).grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self.income_expense_tab, text="Amount", font=font_style).grid(row=2, column=1, padx=10, pady=10)
        self.expense_source = tk.Entry(self.income_expense_tab, font=font_style)
        self.expense_amount = tk.Entry(self.income_expense_tab, font=font_style)
        self.expense_source.grid(row=3, column=0, padx=10, pady=10)
        self.expense_amount.grid(row=3, column=1, padx=10, pady=10)
        tk.Button(self.income_expense_tab, text="Add Expense", font=font_style, command=self.add_expense).grid(row=3, column=2, padx=10, pady=10)

        # Display Data
        tk.Button(self.income_expense_tab, text="Show Data", font=font_style, command=self.show_data).grid(row=4, column=0, columnspan=3, pady=10)

    def add_income(self):
        source = self.income_source.get()
        amount = self.get_amount(self.income_amount.get())
        if source and amount is not None:
            new_row = pd.DataFrame({'Source': [source], 'Amount': [amount]})
            self.income_data = pd.concat([self.income_data, new_row], ignore_index=True)
            self.income_source.delete(0, tk.END)
            self.income_amount.delete(0, tk.END)
            messagebox.showinfo("Info", "Income Added Successfully")
        else:
            messagebox.showerror("Error", "Invalid input for income")

    def add_expense(self):
        source = self.expense_source.get()
        amount = self.get_amount(self.expense_amount.get())
        if source and amount is not None:
            new_row = pd.DataFrame({'Source': [source], 'Amount': [amount]})
            self.expense_data = pd.concat([self.expense_data, new_row], ignore_index=True)
            self.expense_source.delete(0, tk.END)
            self.expense_amount.delete(0, tk.END)
            messagebox.showinfo("Info", "Expense Added Successfully")
        else:
            messagebox.showerror("Error", "Invalid input for expense")

    def create_tax_tab(self):
        font_style = ("Arial", 14)

        tk.Label(self.tax_tab, text="Annual Income", font=font_style).grid(row=0, column=0, padx=10, pady=10)
        self.annual_income = tk.Entry(self.tax_tab, font=font_style)
        self.annual_income.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.tax_tab, text="Calculate Tax", font=font_style, command=self.calculate_tax).grid(row=1, column=0, columnspan=2, pady=10)
        self.tax_result = tk.Label(self.tax_tab, text="", font=font_style)
        self.tax_result.grid(row=2, column=0, columnspan=2, pady=10)

    def calculate_tax(self):
        income = self.get_amount(self.annual_income.get())
        if income is not None:
            if income <= 300000:
                tax = 0
            elif income <= 700000:
                tax = (income - 300000) * 0.05
            elif income <= 1000000:
                tax = (income - 700000) * 0.10 + 20000
            elif income <= 1200000:
                tax = (income - 1000000) * 0.15 + 50000
            elif income <= 1500000:
                tax = (income - 1200000) * 0.20 + 80000
            else:
                tax = (income - 1500000) * 0.30 + 140000
            self.tax_result.config(text=f"Tax Payable: ₹{tax:.2f}")
        else:
            messagebox.showerror("Error", "Invalid input for annual income")

    def create_investment_tab(self):
        font_style = ("Arial", 14)

        tk.Label(self.investment_tab, text="Investment Type", font=font_style).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.investment_tab, text="Amount", font=font_style).grid(row=0, column=1, padx=10, pady=10)
        self.investment_type = tk.Entry(self.investment_tab, font=font_style)
        self.investment_amount = tk.Entry(self.investment_tab, font=font_style)
        self.investment_type.grid(row=1, column=0, padx=10, pady=10)
        self.investment_amount.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.investment_tab, text="Add Investment", font=font_style, command=self.add_investment).grid(row=1, column=2, padx=10, pady=10)

        # Display Data
        tk.Button(self.investment_tab, text="Show Data", font=font_style, command=self.show_investment_data).grid(row=2, column=0, columnspan=3, pady=10)

    def add_investment(self):
        inv_type = self.investment_type.get()
        amount = self.get_amount(self.investment_amount.get())
        if inv_type and amount is not None:
            new_row = pd.DataFrame({'Type': [inv_type], 'Amount': [amount]})
            self.investment_data = pd.concat([self.investment_data, new_row], ignore_index=True)
            self.investment_type.delete(0, tk.END)
            self.investment_amount.delete(0, tk.END)
            messagebox.showinfo("Info", "Investment Added Successfully")
        else:
            messagebox.showerror("Error", "Invalid input for investment")

    def create_budget_tab(self):
        font_style = ("Arial", 14)

        tk.Label(self.budget_tab, text="Monthly Income", font=font_style).grid(row=0, column=0, padx=10, pady=10)
        self.monthly_income = tk.Entry(self.budget_tab, font=font_style)
        self.monthly_income.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.budget_tab, text="Set Budget", font=font_style, command=self.set_budget).grid(row=1, column=0, columnspan=2, pady=10)
        self.budget_result = tk.Label(self.budget_tab, text="", font=font_style)
        self.budget_result.grid(row=2, column=0, columnspan=2, pady=10)

    def set_budget(self):
        income = self.get_amount(self.monthly_income.get())
        if income is not None:
            essentials = income * 0.50
            savings = income * 0.20
            wants = income * 0.30
            self.budget_result.config(text=f"Essentials: ₹{essentials:.2f}, Savings: ₹{savings:.2f}, Wants: ₹{wants:.2f}")
        else:
            messagebox.showerror("Error", "Invalid input for monthly income")

    def show_data(self):
        top = tk.Toplevel(self.root)
        top.title("Income & Expenses Data")
        tk.Label(top, text="Income Data").pack(padx=10, pady=5)
        tk.Label(top, text=self.income_data.to_string(index=False)).pack(padx=10, pady=5)
        tk.Label(top, text="Expense Data").pack(padx=10, pady=5)
        tk.Label(top, text=self.expense_data.to_string(index=False)).pack(padx=10, pady=5)

    def show_investment_data(self):
        top = tk.Toplevel(self.root)
        top.title("Investments Data")
        tk.Label(top, text="Investment Data").pack(padx=10, pady=5)
        tk.Label(top, text=self.investment_data.to_string(index=False)).pack(padx=10, pady=5)

    def get_amount(self, amount_str):
        try:
            return float(amount_str)
        except ValueError:
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalFinanceApp(root)
    root.mainloop()
