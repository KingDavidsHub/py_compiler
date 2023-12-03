import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import subprocess

process = None  # Global variable to store the subprocess

def exec():
    # Get the code from the text widget
    code = text_widget.get("1.0", tk.END)
    
    try:
        global process

        # Execute the code using subprocess
        process = subprocess.Popen(
            ["python", "compiler.py", code],  # Replace "compiler.py" with "-c" to work with Python compiler
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Capture the stdout and stderr of the executed code
        stdout, stderr = process.communicate(input=None)

        # Update the output text widget
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, stdout)
        if stderr:
            output_text.insert(tk.END, stderr, "error")
        output_text.config(state=tk.DISABLED)
    except Exception as e:
        # Handle exceptions and display error messages
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {str(e)}")
        output_text.config(state=tk.DISABLED)

# Create the main Tkinter window
root = tk.Tk()
root.title("Python IDE")

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a "Run" menu with an "Execute" command
run_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="Execute", command=exec)

# Create a scrolled text widget for entering code
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_widget.pack(expand=True, fill='both')
text_widget.configure(font=("TkDefaultFont", 10))

# Create a scrolled text widget for displaying output
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
output_text.pack(expand=True, fill='both')
output_text.tag_configure("error", foreground="red")
output_text.config(state=tk.DISABLED)

# Start the Tkinter event loop
root.mainloop()