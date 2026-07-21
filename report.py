"""This program is generating a report based on the info given by the calling
program
By: Matt Smith                                                    30/06/2026"""

# import modules
from tkinter import messagebox
from datetime import date
import main

# global variables
today = date.today()

# Main program


def report(inventory_list, staff_name):
    # generating reports
    with open(f"report-{today.day}.{today.month}.{today.year}.txt", "w") as \
            report:
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
            total_sold += item[3]
            total_sales += (item[3])*item[5]
            item_name = item[1][:23]  # Truncate name if too long
            report.write(f"{item[0]:<11}{item_name:<24}{item[2]:<7}"
                         f"{item[3]:<8}{(item[2]+item[3]):<8}"
                         f"{item[6]:<8}{item[4]:<6}"
                         f"{((item[2]+item[3])-item[4]-item[6])}\n")
            
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
