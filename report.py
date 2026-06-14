"""This program is generating a report based on the info given by the calling
program
By: Matt Smith                                                    06/05/2026"""

# import modules
from tkinter import messagebox
from datetime import date

# global variables
today = date.today()

# Main program


def report(inventory_list, staff_name):
    # generating reports
    with open(f"report-{today.day}.{today.month}.{today.year}.txt", "w") as report:
        # Header Section
        report.write(f"{'-------------------- Report --------------------':^85}"
                     f"\n{'Barcode':<15} {'Name':<12} {'(Qty)':<10} "
                     f"{'Old':<10} {'Purch':<10} {'Total':<10} {'Sold':<10} "
                     f"{'New':<8} Missing\n")
        report.write("-" * 100 + "\n")

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
            total_sold += item[3]
            total_sales += (item[3])*item[5]
            item_name = item[1][:23]  # Truncate name if too long
            report.write(f"{item[0]:<15} {item_name:<23} {item[2]:<10}"
                         f" {item[3]:<10} {(item[2]+item[3]):<10} "
                         f"{item[6]:<10} {item[4]:<8} "
                         f"{((item[2]+item[3])-item[4]-item[6])}\n")

        report.write("-" * 100 + "\n")

        # Summary Section
        report.write(f"{'Old Stock':<15} {'New Stock':<15} {'Inv. Value':<20} "
                     f"{'Total Sold':<15} {'Sale Price':<15}\n")
        report.write("-" * 100 + "\n")
        report.write(f"{total_old:<15} {total_new:<15} ${inv_value:<19.2f} "
                     f"{total_sold:<15} ${total_sales:<14.2f}\n")

        # Date Footer
        report.write("-" * 100 + "\n")
        report.write(f"Date: {today.day}/{today.month}/{today.year}\n")
        report.write(f"User: {staff_name}\n")
        report.write("-" * 100)

        messagebox.showinfo("Success", "Report saved successfully!")
