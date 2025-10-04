import os
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def run_seqtk(input_file, fasta_width, keep_description, seq_uppercase, progress_bar):

    # Start the progress bar
    progress_bar.start()

    # Change to the input file's directory
    os.chdir(os.path.dirname(input_file))

    # Retrieve filename and extension from input file
    filename, ext = os.path.splitext(os.path.basename(input_file))

    # Create output file
    output_file = f"{filename}.w{fasta_width}{ext}"

    # Create output filepath based on Windows
    output_file_fixed = os.path.join(os.path.dirname(input_file), output_file).replace("/","\\")

    # Select whether or not to convert to uppercase
    up_opt = "U" if seq_uppercase else ""
    
    # Select whether or not to keep descriptiond
    desc_opt = "" if keep_description else "C"

    # Create command
    command = f'seqtk seq -{up_opt}{desc_opt}l{fasta_width} {input_file} > {output_file}'

    try:
        subprocess.run(command, check=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        progress_bar.stop()
        messagebox.showinfo("Success", f"Output file created at: {output_file_fixed}")

    except subprocess.CalledProcessError as e:
        progress_bar.stop()
        messagebox.showerror("Error", f"Failed to run seqkit: {e}")
        
    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("Error", str(e))

def start_thread():
    input_file = input_file_var.get()
    fasta_width = width_var.get()
    keep_description = description_var.get()
    seq_uppercase = uppercase_var.get()
    
    if not input_file:
        messagebox.showwarning("Input Error", "Please select an input file.")
        return

    # Start seqkit command in a new thread
    thread = threading.Thread(target=run_seqtk, args=(input_file, fasta_width, keep_description, seq_uppercase, progress_bar))
    thread.start()

def select_file():
    file_path = filedialog.askopenfilename()
    input_file_var.set(file_path)

# Set up tkinter app
app = tk.Tk()
app.title("Multi FASTA Formatter")

# Input file selection
input_file_var = tk.StringVar()
tk.Label(app, text="Input FASTA file:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(app, textvariable=input_file_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

# Checkbox for additional option
description_var = tk.BooleanVar(value=True)
tk.Checkbutton(app, text="Keep FASTA descriptions", variable=description_var).grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Checkbox for additional option
uppercase_var = tk.BooleanVar(value=True)
tk.Checkbutton(app, text="Convert sequence to uppercase", variable=uppercase_var).grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Fasta width selection
tk.Label(app, text="FASTA Width:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
width_var = tk.StringVar(value="80")
width_options = [0, 60, 80]
width_dropdown = tk.OptionMenu(app, width_var, *width_options)
width_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Progress Bar (indeterminate)
progress_bar = ttk.Progressbar(app, mode="indeterminate", length=200)
progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=20)

# Start button
tk.Button(app, text="Format FASTA", command=start_thread).grid(row=5, column=1, padx=10, pady=20)

# Trademark label
trademark_label = tk.Label(app,  text="Copyright (c) Olga Tsiouri, 2025 <olgatsiouri@outlook.com>", font=("Arial", 10), fg="black")
trademark_label.grid(row=6, column=0, columnspan=3, pady=(20, 10), sticky="s")

app.mainloop()
