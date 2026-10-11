"""This program is generating a report based on the info given by the calling
program
By: Matt Smith                                                    21/08/2026"""

# import modules
from tkinter import messagebox
from datetime import date
import main
import tkinter as tk
from tkinter import filedialog

# global variables
today = date.today()
file = True

# Main program


def report(inventory_list, staff_name):
    """generates reports"""
    global file
    # file location
    while file:
            # Prevent an empty Tkinter window from staying open
        root = tk.Tk()
        root.withdraw()

        # Open the "Save As" window and catch the chosen path
        file_path = filedialog.asksaveasfilename(
            initialdir="/",
            title="Select Save Location",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )

        # Check if the user selected a location or clicked Cancel
        if file_path:
            if file_path.find(".txt") > 0:
                messagebox.showinfo("file location",
                                    f"Valid file path: {file_path}")
                file = False
            else:
                messagebox.showerror("error", "file has to be .txt")
        else:
            messagebox.showerror("error", "Save operation cancelled.")

    # generating reports
    with open(file_path, "w") as report:
        # Header Section
        report.write(f"{'------------------- Report -------------------':>17}"
                     f"\n{'Barcode':<11}{'Name':<14}{'(Qty)':<10}"
                     f"{'Old':<7}{'Purch':<8}{'Total':<8}{'Sold':<8}"
                     f"{'New':<6}Missing\n")
        report.write("-" * 80 + "\n")

        total_old = 0
        total_new = 0
        inv_value = 0.0
        total_sold = 0
        total_sales = 0.0

        # Product Rows
        for names in inventory_list:
            # get names into data
            item = names.description()

            # adding to the to totals
            total_old += item[2]
            total_new += item[6]
            inv_value += (item[6])*item[5]
            total_sold += item[4]
            total_sales += (item[4])*item[5]
            item_name = item[1][:23]  # Truncate name if too long
            report.write(f"{item[0]:<11}{item_name:<24}{item[2]:<7}"
                         f"{item[3]:<8}{(item[2]+item[3]):<8}"
                         f"{item[6]:<8}{item[4]:<6}"
                         f"{(((item[2]+item[3])-item[4]-item[6])*-1)}\n")
            
            main.save_changes("products", "amount", item[4], "barcode", item[0])
            main.save_changes("products", "purchase", 0, "barcode", item[0])
            main.save_changes("products", "count", 0, "barcode", item[0])
            main.save_changes("products", "sold", 0, "barcode", item[0])

        report.write("-" * 80 + "\n")

        # Summary Section
        report.write(f"{'Old Stock':<15} {'New Stock':<15} {'Inv. Value':<20} "
                     f"{'Total Sold':<15} {'Sale Price':<15}\n")
        report.write("-" * 80 + "\n")
        report.write(f"{total_old:<15} {total_new:<15} ${inv_value:<19.2f} "
                     f"{total_sold:<15} ${total_sales:<14.2f}\n")

        # Date Footer
        report.write("-" * 80 + "\n")
        report.write(f"Date: {today.day}/{today.month}/{today.year}\n")
        report.write(f"User: {staff_name}\n")
        report.write("-" * 80)

        messagebox.showinfo("Success", "Report saved successfully!")
