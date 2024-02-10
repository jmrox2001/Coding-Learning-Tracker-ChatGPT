import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

# File to store learning tracker data
DATA_FILE = "learning_tracker_data.json"

# Initialize the learning tracker
learning_tracker = []

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)

def delete_data():
    confirm = messagebox.askyesno("Delete Data", "Are you sure you want to delete the learning tracker data?")
    if confirm:
        try:
            os.remove(DATA_FILE)
            messagebox.showinfo("Success", "Learning tracker data deleted successfully.")
            # Load data after deletion
            load_tracker_data()
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No data file found.")

# Load existing data when the program starts
learning_tracker = load_data()

# Function to display the current learning tracker
def display_learning_tracker():
    learning_list.delete(0, tk.END)  # Clear previous content
    for index, (topic, status, _) in enumerate(learning_tracker, start=1):
        learning_list.insert(tk.END, f"{index}. {topic} - {status}\n")

# Function to add a topic
def add_topic():
    topic = topic_entry.get()
    if topic:
        learning_tracker.append((topic, "Not Started", []))
        display_learning_tracker()
        topic_entry.delete(0, tk.END)  # Clear the entry field
    else:
        messagebox.showwarning("Warning", "Please enter a topic.")

# Function to remove a topic
def remove_topic():
    selected_index = learning_list.curselection()
    if selected_index:
        learning_tracker.pop(selected_index[0])
        display_learning_tracker()

# Function to mark a topic as 'In Progress'
def mark_in_progress():
    selected_index = learning_list.curselection()
    if selected_index:
        topic, status, _ = learning_tracker[selected_index[0]]
        learning_tracker[selected_index[0]] = (topic, "In Progress", [])
        display_learning_tracker()

# Function to mark a topic as 'Completed'
def mark_completed():
    selected_index = learning_list.curselection()
    if selected_index:
        topic, status, _ = learning_tracker[selected_index[0]]
        learning_tracker[selected_index[0]] = (topic, "Completed", [])
        display_learning_tracker()

# Function to handle selecting a topic in the list
def on_select(event):
    selected_index = learning_list.curselection()
    if selected_index:
        topic_entry.delete(0, tk.END)
        topic_entry.insert(0, learning_tracker[selected_index[0]][0])

# Function to save the learning tracker data
def save_tracker_data():
    save_data(learning_tracker)
    messagebox.showinfo("Success", "Learning tracker data saved successfully.")

# Function to load the learning tracker data
def load_tracker_data():
    global learning_tracker
    learning_tracker = load_data()
    display_learning_tracker()
    messagebox.showinfo("Success", "Learning tracker data loaded successfully.")

# Function to ask whether to save data before closing
def on_close():
    if messagebox.askyesno("Save Data", "Do you want to save the learning tracker data before closing?"):
        save_data(learning_tracker)
    root.destroy()


# Create the main window
root = tk.Tk()
root.title("Coding Learning Tracker v3.0")
root.geometry("650x400")
root.resizable(False, True)  # Allow height resizing, disable width resizing

# Create GUI components
topic_label = tk.Label(root, text="Enter Topic:", font=("Helvetica", 12))
topic_entry = tk.Entry(root, width=30, font=("Helvetica", 12))
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", font=("Helvetica", 12))

# Configure colors for buttons
style.map("TButton",
          background=[('active', '#4CAF50'), ('!active', '#2E7D32')],
          foreground=[('active', 'white'), ('!active', 'black')])

add_button = ttk.Button(root, text="Add Topic", command=add_topic, style="TButton", cursor="hand2")
learning_list = tk.Listbox(root, selectmode=tk.SINGLE, width=40, height=10, font=("Helvetica", 12))
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=learning_list.yview)
learning_list.config(yscrollcommand=scrollbar.set)

# Configure colors for buttons
style.map("TButton",
          background=[('active', '#2196F3'), ('!active', '#1565C0')],
          foreground=[('active', 'white'), ('!active', 'black')])

remove_button = ttk.Button(root, text="Remove Topic", command=remove_topic, style="TButton", cursor="hand2")
in_progress_button = ttk.Button(root, text="Mark as In Progress", command=mark_in_progress, style="TButton", cursor="hand2")
completed_button = ttk.Button(root, text="Mark as Completed", command=mark_completed, style="TButton", cursor="hand2")
save_button = ttk.Button(root, text="Save Data", command=save_tracker_data, style="TButton", cursor="hand2")
load_button = ttk.Button(root, text="Load Data", command=load_tracker_data, style="TButton", cursor="hand2")
delete_data_button = ttk.Button(root, text="Delete Data", command=delete_data, style="TButton", cursor="hand2")

# Bind the on_select function to the listbox selection event
learning_list.bind('<<ListboxSelect>>', on_select)

# Bind the on_close function to the window close event
root.protocol("WM_DELETE_WINDOW", on_close)

# Arrange GUI components
topic_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
topic_entry.grid(row=0, column=1, padx=10, pady=10)
add_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.EW)
learning_list.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W+tk.E)
scrollbar.grid(row=1, column=3, sticky=tk.NS)
remove_button.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
in_progress_button.grid(row=2, column=1, padx=10, pady=10)
completed_button.grid(row=2, column=2, padx=10, pady=10)
save_button.grid(row=3, column=0, padx=10, pady=10)
load_button.grid(row=3, column=1, padx=10, pady=10)
delete_data_button.grid(row=3, column=2, padx=10, pady=10)

# Configure row and column weights for resizing
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Run the Tkinter event loop
root.mainloop()
