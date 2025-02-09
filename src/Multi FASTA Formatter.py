import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import textwrap

def run_pipeline(input_file, fasta_width, progress_bar):
    try:
        # Start the progress bar
        progress_bar.start()
    
        # Import fasta file
        with open(input_file, 'r') as file:
            fasta_data = file.read()

        # Split each fasta record
        records = fasta_data.strip().split('>')[1:]

        # reformat each fasta record
        if fasta_width > 0:
            def fasta_record(record):
                # Remove windows line endings
                seqs = str(record).replace("\r","")
                # Retrieve fasta header
                header = str(seqs.split("\n")[0]).strip()
                # Retrieve fasta sequence (-1 is because the last \n leaves an empty string, thus it's removed)
                seq = ''.join(seqs.split("\n")[1:-1])
                # Wrap seq
                wrapped_seq = textwrap.fill(seq,width=fasta_width)
                # Create fasta format output
                fasta_format = f">{header}\n{wrapped_seq}\n"
                return fasta_format
        else:
            def fasta_record(record):
                # Remove windows line endings
                seqs = str(record).replace("\r","")
                # Retrieve fasta header
                header = str(seqs.split("\n")[0]).strip()
                # Retrieve fasta sequence (-1 is because the last \n leaves an empty string, thus it's removed)
                seq = ''.join(seqs.split("\n")[1:-1])
                # Create fasta format output
                fasta_format = f">{header}\n{seq}\n"
                return fasta_format

        # Apply to all fasta records
        wrapped_records = map(fasta_record,records)

        # Export to file
        with open(input_file, 'w') as file:
            for wrapped_record in wrapped_records:
                file.write(wrapped_record)

    
        progress_bar.stop()
        messagebox.showinfo("Success", f"FASTA file reformatted successfully.")
    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("Error", str(e))
        
def start_thread():
    input_file = input_file_var.get()
    fasta_width = width_var.get()

    if not input_file:
        messagebox.showwarning("Input Error", "Please select an input directory.")
        return
    
    # Start command in a new thread
    thread = threading.Thread(target=run_pipeline, args=(input_file, fasta_width, progress_bar))
    thread.start()

def select_file():
    file_path = filedialog.askopenfilename()
    input_file_var.set(file_path)

# Set up tkinter app
app = tk.Tk()
app.title("Multi FASTA Formatter")

# Input file selection
input_file_var = tk.StringVar()
tk.Label(app, text="Input file:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(app, textvariable=input_file_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

# Fasta width selection
tk.Label(app, text="FASTA Width:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
width_var = tk.IntVar(value=80)
width_options = [0, 60, 70, 80]
width_dropdown = tk.OptionMenu(app, width_var, *width_options)
width_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")


# Progress Bar (indeterminate)
progress_bar = ttk.Progressbar(app, mode="indeterminate", length=200)
progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=20)

# Start button
tk.Button(app, text="Run program", command=start_thread).grid(row=3, column=1, padx=10, pady=20)

app.mainloop()
