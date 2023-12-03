import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import subprocess

process = None

def exec():
    code = text_widget.get("1.0", tk.END)
    
    try:
        global process

        process = subprocess.Popen(
            ["python", "compiler.py", code],  # change compiler.py to -c to work with python compiler
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = process.communicate(input=None)


        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, stdout)
        if stderr:
            output_text.insert(tk.END, stderr, "error")
        output_text.config(state=tk.DISABLED)
    except Exception as e:
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {str(e)}")
        output_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Python IDE")


menu_bar = tk.Menu(root)
root.config(menu=menu_bar)


run_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="Execute", command=exec)


text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_widget.pack(expand=True, fill='both')
text_widget.configure(font=("TkDefaultFont", 10))


output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
output_text.pack(expand=True, fill='both')
output_text.tag_configure("error", foreground="red")
output_text.config(state=tk.DISABLED)

root.mainloop()
