import tkinter as tk
import sqlite3
from datetime import datetime

window = tk.Tk()
database = sqlite3.connect("reminders.db")

cursor = database.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reminder TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

database.commit()

window.title("Personal Reminder Application")
window.geometry("600x450")

title_label = tk.Label(window, text="Personal Reminder Application", font=("Times New Roman", 20, "bold"))
title_label.pack(pady=20)

reminder_label = tk.Label(
    window,
    text="Enter your reminder:",
    font=("Times New Roman", 14) 
)
reminder_label.pack()

reminder_entry = tk.Entry(
    window,
    width=40,
    font=("Times New Roman", 14)
)
reminder_entry.pack(pady=10)
date_label = tk.Label(
    window,
    text="Enter date (YYYY-MM-DD):",
    font=("Times New Roman", 14)
)
date_label.pack()

date_entry = tk.Entry(
    window,
    width=20,
    font=("Times New Roman", 14)
)
date_entry.pack(pady=10)

reminder_title = tk.Label(
    window,
    text="Your Reminder:",
    font=("Times New Roman", 14, "bold")
)
reminder_title.pack(pady=5)

reminder_display = tk.Label(
    window,
    text="",
    font=("Times New Roman", 14)
)
reminder_display.pack(pady=10)

reminder_list = tk.Listbox(
    window,
    width=50,
    height=8,
    font=("Times New Roman", 12)
)

reminder_list.pack(pady=10)

def load_reminders():
    cursor.execute("SELECT reminder, date FROM reminders")
    saved_reminders = cursor.fetchall()

    for reminder, date in saved_reminders:
        reminder_list.insert(tk.END, reminder + " - " + date)

load_reminders()

def add_reminder():
    reminder = reminder_entry.get()

    if reminder == "":
        reminder_display.config(text="Please enter a reminder.")
        return
    
    date = date_entry.get()
    if date == "":
     reminder_display.config(text="Please enter a date.")
     return

    try:
      datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
      reminder_display.config(text="Use date format: YYYY-MM-DD")
      return


    cursor.execute(
    "INSERT INTO reminders (reminder, date) VALUES (?, ?)",
    (reminder, date)
)
    database.commit()
    reminder_list.insert(tk.END, reminder + " - " + date)
    reminder_display.config(text=reminder + "\nDate: " + date)

    reminder_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

add_button = tk.Button(
    window,
    text="ADD REMINDER",
    font=("Times New Roman", 13, "bold"),
    command=add_reminder
)
add_button.pack(pady=10)


def delete_reminder():
    selected = reminder_list.curselection()

    if not selected:
        reminder_display.config(text="Please select a reminder.")
        return
    index = selected[0]
    reminder_text = reminder_list.get(index)
    reminder, date = reminder_text.rsplit(" - ", 1)

    cursor.execute(
      "DELETE FROM reminders WHERE reminder = ? AND date = ?",
      (reminder, date)
    )
    database.commit()
    reminder_list.delete(index)

delete_button = tk.Button( 
    window, 
    text="DELETE REMINDER", 
    font=("Times New Roman", 13, "bold"),
    command=delete_reminder
)

delete_button.pack(pady=5)

def edit_reminder():
    selected = reminder_list.curselection()

    if not selected:
        reminder_display.config(text="Please select a reminder.")
        return
    
    index = selected[0]
    reminder_text = reminder_list.get(index)
    reminder, date = reminder_text.rsplit(" - ", 1)
    reminder_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    reminder_entry.insert(0, reminder)
    date_entry.insert(0, date)
    reminder_display.config(text="Edit the reminder and click EDIT REMINDER again.")

edit_button = tk.Button(
    window,
    text="EDIT REMINDER",
    font=("Times New Roman", 13, "bold"),
    command=edit_reminder
)

edit_button.pack(pady=5)


def save_changes():
    selected = reminder_list.curselection()

    if not selected:
        reminder_display.config(text="Please select a reminder.")
        return

    index = selected[0]

    new_reminder = reminder_entry.get()
    new_date = date_entry.get()

    if new_reminder == "":
        reminder_display.config(text="Please enter a reminder.")
        return

    if new_date == "":
        reminder_display.config(text="Please enter a date.")
        return

    try:
        datetime.strptime(new_date, "%Y-%m-%d")
    except ValueError:
        reminder_display.config(text="Use date format: YYYY-MM-DD")
        return

    old_text = reminder_list.get(index)
    old_reminder, old_date = old_text.rsplit(" - ", 1)

    cursor.execute(
        "UPDATE reminders SET reminder = ?, date = ? WHERE reminder = ? AND date = ?",
        (new_reminder, new_date, old_reminder, old_date)
    )

    database.commit()

    reminder_list.delete(index)
    reminder_list.insert(index, new_reminder + " - " + new_date)

    reminder_display.config(text="Reminder updated successfully.")

    reminder_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

save_edit_button = tk.Button(
    window,
    text="SAVE CHANGES",
    font=("Times New Roman", 13, "bold"),
    command=save_changes
)

save_edit_button.pack(pady=5)

window.mainloop()