import matplotlib.pyplot as plt
import datetime
import json
import os
import tkinter as tk
import ttkbootstrap as tb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Expense:
  def __init__(self, name, amount, date, category):
    self.name = name
    self.amount = amount
    self.date = date
    self.category = category
  
  def to_dict(self):
    return {
      "name": self.name,
      "amount": self.amount,
      "date": self.date.isoformat(),
      "category": self.category
    }

expenses = []
if os.path.isfile("expense.json"):
  with open("expense.json", "r") as f:
    data = json.load(f)
    for item in data:
      try:
        parsed_date = datetime.date.fromisoformat(item["date"])
        amount = float(item["amount"])
        expenses.append(Expense(name=item["name"],
                              amount=amount,
                              date=parsed_date,
                              category=item["category"]
                              ))
      except Exception:
        error_messages.config(text="Invalid entry.")
        continue
 
def get_monthly_total(expenses, year, month):
  return sum(e.amount for e in expenses if e.date and e.date.year == year and e.date.month == month)

def get_category_totals(expenses):
  totals = {}
  for e in expenses:
    key = e.category or "Uncategorized"
    totals[key] = totals.get(key, 0) + e.amount
  return totals

def show_expense_chart(expense):
  for widget in output_frame.winfo_children():
    if isinstance(widget, FigureCanvasTkAgg):
      widget.get_tk_widget().destroy()
  
  category_totals = {}
  for e in expense:
    key = e.category or "Uncategorized"
    category_totals[key] = category_totals.get(key, 0) + e.amount

  labels = list(category_totals.keys())
  amount = list(category_totals.values())

  fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
  ax.pie(amount, labels=labels, autopct="%1.1f%%")
  ax.set_title("Expenses by Category")

  canvas = FigureCanvasTkAgg(fig, master=output_frame)
  canvas.draw()
  canvas.get_tk_widget().grid(row=23, column=9, columnspan=2, padx=100, pady=20)

def group_expenses(expenses):
  expenses_dict = {}
  for e in expenses:
    month = e.date.month
    year = e.date.year
    date_format = f"{year}-{month:02d}"
    expenses_dict[date_format] = expenses_dict.get(date_format, 0) + e.amount
  return expenses_dict


def predicted_spending(expenses):
  group = group_expenses(expenses)
  grouped_list = list(group.items())
  sorted_list = sorted(grouped_list, key=lambda x: datetime.datetime.strptime(x[0], "%Y-%m"))
  recent_months = sorted_list[-3:]
  amounts = [amt for _, amt in recent_months]
  if not amounts:
    return 0.0
  else:
    average = (sum(amounts) / len(amounts))
    average = f"Predicted to spend ${average:.2f}"
  prediction_label.config(text=str(average))

def handle_submit():
  name = exp_name.get()
  amount = exp_amount.get()
  date = exp_date.get()
  category = exp_category.get()

  if not name.strip():
    error_messages.config(text="Expense name can't be empty")
    return

  try:
    amount = float(amount)
  except Exception:
    error_messages.config(text="Invalid amount entry. Please enter a proper amount")
    return

  if date:
    try:
      parsed_date = datetime.datetime.strptime(date, "%m/%d/%y").date()
      # exp_date_label.config(text=parsed_date.strftime("%m/%d/%y"))
    except Exception:
      error_messages.config(text="Invalid date format. Please use MM/DD/YY format")
      return
  else:
    parsed_date = datetime.date.today()
  
  if not category:
    category = "Uncategorized"
  
  new_expense = Expense(name, amount, parsed_date, category)
  expenses.append(new_expense)

  with open("expense.json", "w") as f:
    json.dump([e.to_dict() for e in expenses], f, indent=2)

  today = datetime.date.today()
  monthly_total = get_monthly_total(expenses, today.year, today.month)
  total_label.config(text=f"Total spent this month is: ${monthly_total:.2f}")
  
  category_totals = get_category_totals(expenses)
  breakdown = "\n".join([f"{cat}: ${amt:.2f}" for cat, amt in category_totals.items()])
  category_label.config(text=breakdown)

  exp_name.delete(0, tk.END)
  exp_amount.delete(0, tk.END)
  exp_date.delete(0, tk.END)
  exp_category.delete(0, tk.END)
  error_messages.config(text="")

def main():
  # GUI - Tkinter
  global window, main_frame, input_frame, summary_frame, button_frame, output_frame, error_messages
  global exp_name, exp_amount, exp_date, exp_category
  global total_label, category_label, prediction_label

  window = tb.Window(themename="darkly")
  window.geometry("1500x750")
  window.title("Expenses Tracker") 
  # window.config(bg="#1e1e1e")
  window.bind("<Return>", lambda event: handle_submit())

  # Main Frame
  main_frame = tk.Frame(window, bg="#2c2c2c")
  main_frame.pack(anchor="w", padx=20, pady=20)

  # Input Frame
  input_frame = tk.Frame(main_frame, bg="#2c2c2c")
  input_frame.grid(row=0, column=0, columnspan=4, pady=(10, 20))

  # Input Frame
  summary_frame = tk.Frame(main_frame, bg="#2c2c2c")
  summary_frame.grid(row=0, column=4, columnspan=4, pady=(10, 20))

  # Button Frame
  button_frame = tk.Frame(input_frame, bg="#2c2c2c")
  button_frame.grid(row=9, column=0, columnspan=4, pady=(10, 20))

  # Output Frame
  output_frame = tk.Frame(main_frame, bg="#2c2c2c")
  output_frame.grid(row=0, column=9, columnspan=4)

  # Error message
  error_messages = tk.Label(main_frame, text="", font=("Segoe UI", 12))
  error_messages.grid(row=12, column=0, padx=10, pady=5)

  # Text for screen

  title_label = tk.Label(input_frame, text="Expense Tracker", font=("Segoe UI", 22, "bold"))
  title_label.grid(row=0, column=1, columnspan=4, pady=(20, 10))

  # section_label = tk.Label(main_frame, text="Enter New Expense", font=("Segoe UI", 14, "bold"), bg="#3c3c3c", fg="white", highlightthickness=0)
  # section_label.grid(row=0, column=1, columnspan=2, pady=(10, 0))

  name_label = tk.Label(input_frame, text="Expense name", font=("Segoe UI", 12), bg="#3c3c3c", fg="white", highlightthickness=0)
  name_label.grid(row=1, column=0, padx=0, pady=5)

  amount_label = tk.Label(input_frame, text="Amount", font=("Segoe UI", 12), bg="#3c3c3c", fg="white", highlightthickness=0)
  amount_label.grid(row=3, column=0, padx=0, pady=5)

  date_label = tk.Label(input_frame, text="Date", font=("Segoe UI", 12), bg="#3c3c3c", fg="white", highlightthickness=0)
  date_label.grid(row=5, column=0, padx=0, pady=5)

  category_label = tk.Label(input_frame, text="Category", font=("Segoe UI", 12), bg="#3c3c3c", fg="white", highlightthickness=0)
  category_label.grid(row=7, column=0, padx=0, pady=5)

  # Prompting user for expense inputs

  exp_name = tk.Entry(input_frame, width=35)
  exp_name.grid(row=2, column=0, padx=10, pady=(5, 13), sticky="w", ipady=5)

  exp_amount = tk.Entry(input_frame, width=35)
  exp_amount.grid(row=4, column=0, padx=10, pady=(5, 13), sticky="w", ipady=5)

  exp_date = tk.Entry(input_frame, width=35)
  exp_date.grid(row=6, column=0, padx=10, pady=(5, 13), sticky="w", ipady=5)

  exp_category = tk.Entry(input_frame, width=35)
  exp_category.grid(row=8, column=0, padx=10, pady=(5, 13), sticky="w", ipady=5)

  # Submit button

  enter_button = tb.Button(button_frame, text="Enter", bootstyle="secondary", command=handle_submit)
  enter_button.grid(row=9, column=0, padx=10, pady=(20, 10), sticky="ew")

  # Chart button

  chart_button = tb.Button(button_frame, text="Show Chart", bootstyle="secondary", command=lambda: show_expense_chart(expenses))
  chart_button.grid(row=9, column=1, padx=10, pady=(20, 10), sticky="ew")

  # Predictive button
  predicted_button = tb.Button(button_frame, text="Predict spending for the next 3 months", bootstyle="secondary", command=lambda: predicted_spending(expenses))
  predicted_button.grid(row=9, column=2, padx=10, pady=(20, 10), sticky="ew")

  # Total label
  total_label = tk.Label(summary_frame, text="Total spent this month will appear here", font=("Segoe UI", 16),)
  total_label.grid(row=10, column=0, padx=10, pady=(60, 10), sticky="w")

  # Category label
  category_label = tk.Label(summary_frame, text="Category total will appear here", font=("Segoe UI", 16),)
  category_label.grid(row=11, column=0, padx=10, pady=(60, 10), sticky="w")

  # Prediction label
  prediction_label = tk.Label(summary_frame, text="Predicted spending will appear here", font=("Segoe UI", 16),)
  prediction_label.grid(row=12, column=0, padx=10, pady=(60, 10), sticky="w")

  window.mainloop()

if __name__ == "__main__":
    main()
