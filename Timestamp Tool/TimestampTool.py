import tkinter as tk
from tkinter import messagebox

# Function to convert minutes and seconds to total seconds
def convert_to_seconds():
    try:
        minutes = int(entry_minutes.get())
        seconds = int(entry_seconds.get())
        
        # Validate input
        if minutes < 0 or seconds < 0:
            raise ValueError("Negative values are not allowed.")
        
        # Total seconds calculation
        total_seconds = minutes * 60 + seconds
        label_result.config(text=f"Total seconds: {total_seconds}")
        
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")

# Setting up the GUI window
root = tk.Tk()
root.title("Timestamp Tool")

# Create labels, entries, and buttons
label_minutes = tk.Label(root, text="Minutes:")
label_minutes.grid(row=0, column=0, padx=10, pady=10)

entry_minutes = tk.Entry(root)
entry_minutes.grid(row=0, column=1, padx=10, pady=10)

label_seconds = tk.Label(root, text="Seconds:")
label_seconds.grid(row=1, column=0, padx=10, pady=10)

entry_seconds = tk.Entry(root)
entry_seconds.grid(row=1, column=1, padx=10, pady=10)

# Button to trigger the conversion
button_convert = tk.Button(root, text="Convert", command=convert_to_seconds)
button_convert.grid(row=2, column=0, columnspan=2, pady=10)

# Label to display the result
label_result = tk.Label(root, text="Total seconds: 0")
label_result.grid(row=3, column=0, columnspan=2, pady=10)

# Run the main loop
root.mainloop()
