import pandas as pd
import os
import sys

def convert_txt_to_xlsx():
    print("--- TXT to XLSX Converter (With Data Scaling) ---\n")

    # 1. Setup Environment
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Working in directory: {script_dir}\n")

    # 2. Get Filename
    filename = input("Enter the filename (e.g., data.txt): ").strip().strip('"')
    file_path = os.path.join(script_dir, filename)

    if not os.path.exists(file_path):
        print(f"\nError: Could not find '{filename}' in the folder.")
        input("Press Enter to exit...")
        return

    # 3. Get Data Configuration
    try:
        start_row = int(input("Enter the starting row number for the DATA (e.g. 3): "))
        if start_row < 1: raise ValueError
        
        num_columns = int(input("Enter the number of data columns: "))
        if num_columns < 1: raise ValueError
    except ValueError:
        print("Error: Row and Column counts must be positive integers.")
        input("Press Enter to exit...")
        return

    # 4. Get Scaling Factors (New Feature)
    print("\n--- Data Scaling ---")
    print("You can multiply each column by a factor (e.g. -1 to invert, 1000 for units).")
    apply_scale = input("Do you want to apply scaling factors? (y/n): ").strip().lower()

    factors = []
    if apply_scale.startswith('y'):
        while True:
            print(f"\nPlease enter {num_columns} numbers separated by spaces.")
            print("Example for 3 cols:  1.0  -1  0.5")
            user_factors = input("Factors: ")
            
            try:
                # Convert string input "1 -1 0.5" into a list of floats [1.0, -1.0, 0.5]
                factors = [float(x) for x in user_factors.split()]
                
                if len(factors) != num_columns:
                    print(f"Error: You entered {len(factors)} factors, but defined {num_columns} columns.")
                    continue
                break # Break loop if input is valid
            except ValueError:
                print("Error: Inputs must be numbers (integers or decimals).")
    else:
        # If no scaling, create a list of 1.0s (neutral multiplication)
        factors = [1.0] * num_columns


    # 5. Process the File
    output_filename = os.path.splitext(filename)[0] + ".xlsx"
    output_path = os.path.join(script_dir, output_filename)

    try:
        print(f"\nReading '{filename}'...")

        # --- Part A: Headers (Metadata) ---
        header_rows_count = start_row - 1
        df_headers = pd.DataFrame()

        if header_rows_count > 0:
            df_headers = pd.read_csv(
                file_path,
                sep=r'\s+',
                header=None,
                nrows=header_rows_count,
                usecols=range(num_columns),
                engine='python'
            ).fillna('')

        # --- Part B: Data (Numeric) ---
        df_data = pd.read_csv(
            file_path,
            sep=r'\s+',
            header=None,
            skiprows=header_rows_count,
            usecols=range(num_columns),
            engine='python'
        )

        # --- Part C: Apply Scaling ---
        # We multiply the dataframe by the list of factors
        # Pandas matches the list index to the column index automatically
        print("Applying scaling factors...")
        df_data = df_data.multiply(factors, axis=1)

        # --- Part D: Save ---
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Write headers
            if not df_headers.empty:
                df_headers.to_excel(writer, index=False, header=False, startrow=0)
            
            # Write data
            df_data.to_excel(writer, index=False, header=False, startrow=header_rows_count)

        print(f"Success! Created: {output_filename}")
        if apply_scale.startswith('y'):
            print(f"Applied factors: {factors}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Tip: Ensure your 'Data Rows' contain only numbers, not text.")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    convert_txt_to_xlsx()