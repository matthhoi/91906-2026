import tkinter as tk
from tkinter import ttk
import main
import report

BUTTONS = "#C5C2D0"
BG_COLOR = "#cccccc"
BLACK = "#000000"

inventory_list = []

# inventory count
def make_report():
    """get all the info from the database and add that info to the report"""
    staff_name = main.staff_name
    # connect with the database and get the products info
    results = main.connect_with_database("""SELECT * from products;""", 1)
    
    # put the results into the products .py function
    for x in range(0, len(results)):
        product = main.products.products(results[x][0], results[x][8],
                                    results[x][2], results[x][2],
                                    results[x][3], results[x][4])
        product.stock_sold(results[x][5])
        product.inventory_count(results[x][7])
        product.stock_purchase(results[x][6])
        # put the item in the list
        inventory_list.append(product)
    # run the report program
    report.report(inventory_list, staff_name)

def inventory_count(frame):
    """All the buttons and labels for the count_frame"""
    # labels
    Select_label = tk.Label(frame, text="Select product", 
                          font=('Arial', 20,"bold"), bg=BG_COLOR) 
    Select_label.place(x=40, y=50)
    num_of_label = tk.Label(frame, text="Number of product", 
                          font=('Arial', 20,"bold"), bg=BG_COLOR) 
    num_of_label.place(x=300, y=50)
    
    # entries
    num_entry = tk.Entry(frame, font=('Arial', 15,"bold"), bg=BUTTONS)
    num_entry.place(x=310, y=150, height=40)
    
    # combo box data
    options = main.combo_data("name", "Products")

    # create the combo box
    combo = ttk.Combobox(frame, values=options, font=('Arial', 15))
    combo.place(x=30, y=150, height=40)

    # Bind key release to the search function
    combo.bind('<KeyRelease>', lambda event: main.on_type(event, combo,
                                                          options))
    combo.bind('<Return>', lambda event: main.validate(event, num_entry,
                                                       combo, options, 1))
    num_entry.bind('<Return>', lambda event: main.validate(event, num_entry,
                                                           combo, options, 1))

    # buttons
    gen_report =  tk.Button(frame, text="Generate report", cursor="hand2", 
                            font=('Arial', 17,"bold"), bg=BUTTONS, width=19,
                            height=3, highlightcolor=BLACK, bd=1, 
                            relief="solid", command=lambda: make_report())
    gen_report.place(x=590, y=350)
    Save_changes =  tk.Button(frame, text="Save changes", cursor="hand2", 
                            font=('Arial', 17,"bold"), bg=BUTTONS, width=19,
                            height=3, highlightcolor=BLACK, bd=1, 
                            relief="solid", command=lambda event=None: 
                            main.validate(event, num_entry, combo, options, 1))
    Save_changes.place(x=590, y=25)
