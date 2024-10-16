import tkinter as tk
from tkinter import ttk
import math

class AdvancedCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Calculator")
        self.master.geometry("400x550")
        self.master.minsize(300, 400)  # Set minimum size
        self.master.resizable(True, True)  # Allow resizing in both directions

        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.history = []

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12))

        # Result display
        result_frame = ttk.Frame(self.master, padding="10")
        result_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")

        result_display = ttk.Entry(result_frame, textvariable=self.result_var, font=("Arial", 20), justify="right", state="readonly")
        result_display.pack(fill=tk.X)

        # Button layout
        button_frame = ttk.Frame(self.master, padding="10")
        button_frame.grid(row=1, column=0, columnspan=5, sticky="nsew")

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('C', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('√', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('^', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3), ('π', 4, 4),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('log', 5, 3), ('exp', 5, 4)
        ]

        for (text, row, col) in buttons:
            ttk.Button(button_frame, text=text,
                       command=lambda x=text: self.button_click(x)).grid(row=row,
                       column=col, sticky="nsew", padx=2, pady=2)

        # Configure grid weights for resizing
        for i in range(5):
            button_frame.columnconfigure(i, weight=1)
        for i in range(6):
            button_frame.rowconfigure(i, weight=1)

        # History display
        history_frame = ttk.Frame(self.master, padding="10")
        history_frame.grid(row=6, column=0, columnspan=5, sticky="nsew")

        history_label = ttk.Label(history_frame, text="History:", font=("Arial", 12))
        history_label.pack(anchor="w")

        self.history_display = tk.Text(history_frame,
                                       height=5,
                                       width=40,
                                       font=("Arial", 10),
                                       state="disabled")
        self.history_display.pack(fill=tk.BOTH)

    def button_click(self, key):
        if key == '=':
            self.evaluate_expression()
        elif key == 'C':
            self.result_var.set("0")
        elif key in ['sin', 'cos', 'tan', 'log', 'exp', '√']:
            self.calculate_function(key)
        elif key == 'π':
            self.result_var.set(str(math.pi))
        else:
            self.update_display(key)

    def evaluate_expression(self):
        try:
            expression = self.result_var.get().replace('^', '**') # Handle exponentiation
            result = eval(expression)
            if isinstance(result, complex): # Handle complex numbers if needed
                raise ValueError("Complex results not supported.")
            self.history.append(f"{expression} = {result}")
            self.result_var.set(result)
            self.update_history()
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")

    def calculate_function(self, func):
        try:
            value = float(self.result_var.get())
            result = {
                'sin': math.sin(value),
                'cos': math.cos(value),
                'tan': math.tan(value),
                'log': math.log10(value) if value > 0 else "Error",
                'exp': math.exp(value),
                '√': math.sqrt(value) if value >= 0 else "Error"
            }.get(func)

            if isinstance(result, str): # If it's an error message
                raise ValueError(result)

            self.history.append(f"{func}({value}) = {result}")
            self.result_var.set(result)
            self.update_history()
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")

    def update_display(self, key):
        current_value = self.result_var.get()
        
        if current_value in ["0", "Error"]:
            self.result_var.set(key)
        else:
            self.result_var.set(current_value + key)

    def update_history(self):
        """Update the history display with the last five operations."""
        self.history_display.config(state="normal")
        self.history_display.delete('1.0', tk.END)
        
        for item in self.history[-5:]:  
            self.history_display.insert(tk.END, item + "\n")
        
        self.history_display.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop()