import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Single TXT to Excel Converter")
        self.root.geometry("600x450")
        
        # Variable to store the single file path
        self.selected_file_path = None
        
        # --- UI Layout ---
        
        # 1. File Selection Section
        frame_files = tk.LabelFrame(root, text="Step 1: Select File", padx=10, pady=10)
        frame_files.pack(fill="x", padx=10, pady=5)
        
        # Button to browse
        self.btn_browse = tk.Button(frame_files, text="Browse File...", command=self.browse_file)
        self.btn_browse.grid(row=0, column=0, padx=(0, 10))
        
        # Entry box to display the file path (ReadOnly)
        self.ent_filepath = tk.Entry(frame_files, width=60, state='readonly')
        self.ent_filepath.grid(row=0, column=1)

        # 2. Configuration Section
        frame_config = tk.LabelFrame(root, text="Step 2: Configuration", padx=10, pady=10)
        frame_config.pack(fill="x", padx=10, pady=5)
        
        # Start Row
        tk.Label(frame_config, text="Start Row of DATA (integer):").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_start_row = tk.Entry(frame_config)
        self.ent_start_row.grid(row=0, column=1, pady=5, padx=10)
        self.ent_start_row.insert(0, "1") # Default
        
        # Num Columns
        tk.Label(frame_config, text="Number of Columns:").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_cols = tk.Entry(frame_config)
        self.ent_cols.grid(row=1, column=1, pady=5, padx=10)
        
        # Scaling Factors
        tk.Label(frame_config, text="Scaling Factors (Optional):").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_factors = tk.Entry(frame_config, width=30)
        self.ent_factors.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(frame_config, text="(e.g: 1 -1 1000)", font=("Arial", 8), fg="gray").grid(row=2, column=2, sticky="w")

        # 3. Action Section
        self.btn_convert = tk.Button(
            root, 
            text="CONVERT TO EXCEL", 
            command=self.convert_file, 
            bg="#E1E1E1", 
            font=("Arial", 10, "bold")
        )
        self.btn_convert.pack(pady=20, ipadx=20, ipady=5)

        # 4. Success Message Area
        self.lbl_status = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.lbl_status.pack(pady=10)

    def browse_file(self):
        # Allow only single file selection
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        
        if file_path:
            self.selected_file_path = file_path
            
            # Update the display box
            self.ent_filepath.config(state='normal') # Enable to write
            self.ent_filepath.delete(0, tk.END)
            self.ent_filepath.insert(0, file_path)
            self.ent_filepath.config(state='readonly') # Disable again
            
            # Reset status message
            self.lbl_status.config(text="", fg="black")

    def convert_file(self):
        # Clear previous status
        self.lbl_status.config(text="")

        # 1. Validation
        if not self.selected_file_path:
            messagebox.showwarning("Warning", "Please select a file first.")
            return

        try:
            start_row = int(self.ent_start_row.get())
            num_cols = int(self.ent_cols.get())
            if start_row < 1 or num_cols < 1: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Start Row and Columns must be positive integers.")
            return

        # 2. Parse Scaling Factors
        factors = []
        raw_factors = self.ent_factors.get().strip()
        if raw_factors:
            try:
                factors = [float(x) for x in raw_factors.split()]
                if len(factors) != num_cols:
                    messagebox.showerror("Error", f"You entered {len(factors)} factors for {num_cols} columns.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Factors must be numbers separated by spaces.")
                return
        else:
            factors = [1.0] * num_cols

        # 3. Process the single file
        try:
            self.process_conversion(self.selected_file_path, start_row, num_cols, factors)
            
            # Update the Status Label on Success
            self.lbl_status.config(text="Conversion Successful!", fg="green")
            
        except Exception as e:
            self.lbl_status.config(text="Conversion Failed", fg="red")
            messagebox.showerror("Error", str(e))

    def process_conversion(self, file_path, start_row, num_cols, factors):
        filename = os.path.basename(file_path)
        folder = os.path.dirname(file_path)
        output_path = os.path.join(folder, os.path.splitext(filename)[0] + ".xlsx")

        header_rows_count = start_row - 1
        
        # Read Headers (Metadata)
        df_headers = pd.DataFrame()
        if header_rows_count > 0:
            df_headers = pd.read_csv(
                file_path, sep=r'\s+', header=None, nrows=header_rows_count, 
                usecols=range(num_cols), engine='python'
            ).fillna('')

        # Read Data
        df_data = pd.read_csv(
            file_path, sep=r'\s+', header=None, skiprows=header_rows_count, 
            usecols=range(num_cols), engine='python'
        )

        # Apply Scaling
        df_data = df_data.multiply(factors, axis=1)

        # Save to Excel
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            if not df_headers.empty:
                df_headers.to_excel(writer, index=False, header=False, startrow=0)
            df_data.to_excel(writer, index=False, header=False, startrow=header_rows_count)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()