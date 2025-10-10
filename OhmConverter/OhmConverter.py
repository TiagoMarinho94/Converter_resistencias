import pandas as pd
import tkinter as tk
from tkinter import filedialog
import re

# Function to convert values to ohms
def convert_to_ohms(value, unit):
    unit = str(unit).strip().lower()
    val_str = str(value).strip().replace(' ', '')

    # Handle 'OL' case
    if val_str.upper() == "OL":
        print("Value is 'OL'. Converting to 100000000 Ohms.")
        return 100_000_000

    # Remove non-numeric symbols except commas, dots, and minus sign
    val_str = re.sub(r'[^0-9,.\-]', '', val_str)

    # Convert comma to dot for decimal conversion
    val_str = val_str.replace(',', '.')

    try:
        val = float(val_str)
    except ValueError:
        print(f"Non-numeric value encountered: {value}. Skipping conversion.")
        return value  # skip if not numeric

    # Handle kiloohms and megaohms
    if any(u in unit for u in ['k', 'kω', 'kΩ', 'kilo']):
        converted_value = val * 1e3
    elif any(u in unit for u in ['m', 'mω', 'mΩ', 'mega']):
        converted_value = val * 1e6
    else:
        converted_value = val  # already ohms

    print(f"Converted value: {converted_value} Ohms")
    return int(round(converted_value))

# Use tkinter to prompt the user to select an Excel file
root = tk.Tk()
root.withdraw()  # Hide the root window
file_path = filedialog.askopenfilename(
    title="Select an Excel file",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)

# Load the selected Excel file
if file_path:
    df = pd.read_excel(file_path)
    print("Column names in the Excel file:", df.columns)  # Debugging output

    # Replace 'Value' and 'Unit' with actual column names if different
    if 'Value' in df.columns and 'Unit' in df.columns:
        # Apply the conversion function to each row
        df['Value in Ohms'] = df.apply(lambda row: convert_to_ohms(row['Value'], row['Unit']), axis=1)

        # Ensure the output file extension is correct
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            output_file = file_path.rsplit('.', 1)[0] + '_converted.xlsx'
        else:
            output_file = file_path + '_converted.xlsx'

        # Save the result to a new Excel file
        df.to_excel(output_file, index=False)

        print(f"Converted values saved to {output_file}")
    else:
        print("Error: The required columns 'Value' and/or 'Unit' were not found.")
else:
    print("No file selected.")