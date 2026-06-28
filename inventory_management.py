import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import main

# constants
BUTTONS = "#C5C2D0"
BG_COLOR = "#cccccc"
LABEL_COLOR = "#efefef"
BLACK = "#000000"

# inventory management
def add(event, barcode, name, type, cost, amount, display):
    """validate the entries and update the database"""

    # see is barcode is already in the database
    results = main.connect_with_database(f"""SELECT barcode FROM products 
                                         WHERE barcode = "{barcode.get()}";""",
                                         1)
    if results == []:
        ask = True
    else:
        # ask if the user wishes to change the current entry
        ask = messagebox.askyesno("Warning", "This barcode already " \
        "exists do you want to override this entry")
        if ask == True:
            main.connect_with_database(f"""DELETE FROM Products WHERE barcode 
                                       = "{barcode.get()}";""", 2)
    
    # see if any of the entries are empty
    if name.get() == "" or type.get() == "" or display.get() == "":
        messagebox.showerror("error", "Entries can not be blank")
    else:
        try:
            # see if any of the barcode, cost, and amount are numbers
            if ask == True and barcode.get().isdigit() and float(cost.get()) \
                and amount.get().isdigit():
                # create a new entry and delete the entries
                main.connect_with_database(f"""INSERT INTO products (barcode, 
                                           name, type, cost, amount, display_
                                           name) VALUES ({barcode.get()}, 
                                           "{name.get()}", "{type.get()}", 
                                           {cost.get()}, {amount.get()}, 
                                           "{display.get()}");""", 2)
                # reset the entries
                barcode.delete(0, tk.END)
                name.delete(0, tk.END)
                type.delete(0, tk.END)
                cost.delete(0, tk.END)
                amount.delete(0, tk.END)
                display.delete(0, tk.END)
            else:
                if ask == True:
                    messagebox.showerror("error", "Barcode and or amount " \
                                         "have to be numbers or Entries can " \
                                         "not be blank")
        except:
            messagebox.showerror("error", f"cost has to be a number")

def add_product(frame):
    """All the buttons and labels for adding a product in mang_frame"""
    
    # labels
    barcode_label = tk.Label(frame, text="Barcode",
                            font=('Arial', 12,"bold"), bg=BG_COLOR)
    barcode_label.place(x=20, y=23)
    name_label = tk.Label(frame, text="Name", font=('Arial', 12,"bold"),
                          bg=BG_COLOR)
    name_label.place(x=25, y=123)
    type_label = tk.Label(frame, text="Type", font=('Arial', 12,"bold"),
                          bg=BG_COLOR)
    type_label.place(x=25, y=223)
    cost_label = tk.Label(frame, text="Cost", font=('Arial', 12,"bold"),
                          bg=BG_COLOR)
    cost_label.place(x=380, y=23)
    amount_label = tk.Label(frame, text="Amount", font=('Arial', 12,"bold"),
                            bg=BG_COLOR)
    amount_label.place(x=370, y=123)
    display_label = tk.Label(frame, text="display\nname", 
                             font=('Arial', 12,"bold"),bg=BG_COLOR)
    display_label.place(x=370, y=223)

    # entries
    barcode_entry = tk.Entry(frame, font=('Arial', 15,"bold"), bg=BUTTONS)
    barcode_entry.place(x=110, y=20, height=40)
    name_entry = tk.Entry(frame, font=('Arial', 15,"bold"), bg=BUTTONS)
    name_entry.place(x=110, y=120, height=40)
    type_entry = tk.Entry(frame, font=('Arial', 15,"bold"), bg=BUTTONS)
    type_entry.place(x=110, y=220, height=40)
    cost_entry = tk.Entry(frame, font=('Arial', 15,"bold"), bg=BUTTONS)
    cost_entry.place(x=470, y=20, height=40)
    amount_entry = tk.Entry(frame, font=('Arial', 15,"bold"), bg=BUTTONS)
    amount_entry.place(x=470, y=120, height=40)
    display_entry = tk.Entry(frame, font=('Arial', 15,"bold"), bg=BUTTONS)
    display_entry.place(x=470, y=220, height=40)

    barcode_entry.bind('<Return>', lambda event: add(event, barcode_entry, 
                       name_entry, type_entry, cost_entry, amount_entry, 
                       display_entry))
    name_entry.bind('<Return>', lambda event: add(event, barcode_entry, 
                       name_entry, type_entry, cost_entry, amount_entry, 
                       display_entry))
    type_entry.bind('<Return>', lambda event: add(event, barcode_entry, 
                       name_entry, type_entry, cost_entry, amount_entry, 
                       display_entry))
    cost_entry.bind('<Return>', lambda event: add(event, barcode_entry, 
                       name_entry, type_entry, cost_entry, amount_entry, 
                       display_entry))
    amount_entry.bind('<Return>', lambda event: add(event, barcode_entry, 
                       name_entry, type_entry, cost_entry, amount_entry, 
                       display_entry))
    display_entry.bind('<Return>', lambda event: add(event, barcode_entry, 
                       name_entry, type_entry, cost_entry, amount_entry, 
                       display_entry))

    # buttons
    update =  tk.Button(frame, text="Save\nchanges", cursor="hand2",
                        font=('Arial', 15,"bold"), bg=BUTTONS, width=12,
                        height=2, highlightcolor=BLACK, bd=1, relief="solid",
                        command=lambda event=None: add(event, barcode_entry, 
                        name_entry, type_entry, cost_entry, amount_entry, 
                        display_entry))
    update.place(x=710, y=210)

def remove(event, combo, options):
    """validate the entries and update the database"""
        # validate entries
    if combo.get() in options:
        yes_no = messagebox.askyesno("warning", "This action can NOT be "
                                     "undone are you sure?")
        if yes_no == True:
            main.connect_with_database(f"""DELETE FROM Products WHERE name = 
                                  "{combo.get()}";""", 2)
            messagebox.showinfo("success", "successfully updated database")
            combo.delete(0, tk.END)
    else:
        messagebox.showerror("error", "product has to be in options")

def remove_product(frame):
    """All the buttons and labels for remove product in mang_frame"""
    
    # combo box data
    options = main.combo_data("name", "Products")

    # create the combo box
    combo = ttk.Combobox(frame, values=options, font=('Arial', 15))
    combo.place(x=300, y=200, height=40)

    # Bind key release to the search function
    combo.bind('<KeyRelease>', lambda event: main.on_type(event, combo, 
                                                          options))
    combo.bind('<Return>', lambda event: remove(event, combo, options))

    # buttons
    update =  tk.Button(frame, text="remove product", cursor="hand2",
                        font=('Arial', 17,"bold"), bg=BUTTONS, width=19,
                        height=3, highlightcolor=BLACK, bd=1, relief="solid",
                        command=lambda event=None: remove(event, combo, 
                                                          options))
    update.place(x=290, y=25)

def purchase(event, num_entry, combo, options, cost_entry):
    """validate the entries and get the data need to update the database"""
    # validate entries
    try:
        if num_entry.get().isdigit() and combo.get() in options and \
            float(cost_entry.get()):
            if float(cost_entry.get()) > 0:
                results = main.connect_with_database(f"""SELECT cost, amount, 
                                                purchase FROM Products WHERE 
                                                name = "{combo.get()}";""", 1)
                
                current_total_value = results[0][1] * results[0][0]
                new_total_value = int(num_entry.get()) * \
                    float(cost_entry.get())
                total_quantity = results[0][2] + int(num_entry.get())
                total_value = current_total_value + new_total_value
                new_cost = total_value / total_quantity
                main.save_changes("Products", "cost", new_cost, "name",
                                  combo.get())
                main.save_changes("Products", "purchase", total_quantity,
                                  "name" , combo.get())
                num_entry.delete(0, tk.END)
                combo.delete(0, tk.END)
                cost_entry.delete(0, tk.END)
                messagebox.showinfo("success", "successfully updated database")
            else:
                messagebox.showerror("error", "cost has to be a positive "
                                     "number")
        else:
            messagebox.showerror("error", "Number of products has to be a "
                                 "number and or product has to be selected")
    except:
        messagebox.showerror("error", f"cost has to be a number")

def product_purchase(frame):
    """All the buttons and labels for product purchase in mang_frame"""

    # labels
    select_label = tk.Label(frame, text="Select product", 
                            font=('Arial', 20,"bold"), bg=BG_COLOR)
    select_label.place(x=620, y=150)
    amount_label = tk.Label(frame, text="Amount \npurchased", 
                            font=('Arial', 20,"bold"), bg=BG_COLOR)
    amount_label.place(x=60, y=80)
    cost_label = tk.Label(frame, text="Cost", 
                          font=('Arial', 20,"bold"), bg=BG_COLOR)
    cost_label.place(x=80, y=200)

    # entries
    num_entry = tk.Entry(frame, font=('Arial', 15,"bold"), bg=BUTTONS)
    num_entry.place(x=300, y=100, height=40)
    cost_entry = tk.Entry(frame, font=('Arial', 15,"bold"), bg=BUTTONS)
    cost_entry.place(x=300, y=200, height=40)

    # combo box data
    options = main.combo_data("name", "Products")

    # create the combo box
    combo = ttk.Combobox(frame, values=options, font=('Arial', 15))
    combo.place(x=600, y=200, height=40)

    # Bind key release to the search function
    combo.bind('<KeyRelease>', lambda event: main.on_type(event, combo, 
                                                          options))
    combo.bind('<Return>', lambda event: main.validate(event, num_entry,
                                                       combo, options, 2))
    num_entry.bind('<Return>', lambda event: main.validate(event, num_entry,
                                                           combo, options, 2))
    cost_entry.bind('<Return>', lambda event: main.validate(event, num_entry,
                                                            combo, options, 2))

    # buttons
    save_changes =  tk.Button(frame, text="Save changes", cursor="hand2", 
                              font=('Arial', 17,"bold"), bg=BUTTONS, width=19,
                              height=3, highlightcolor=BLACK, bd=1, 
                              relief="solid", command=lambda event=None: 
                              purchase(event ,num_entry, combo, options, 
                                       cost_entry))
    save_changes.place(x=590, y=25)

def stock_sold(frame):
    """All the buttons and labels for stock sold in mang_frame"""

    # labels
    Select_label = tk.Label(frame, text="Select product", 
                            font=('Arial', 20,"bold"), bg=BG_COLOR)
    Select_label.place(x=320, y=50)
    amount_label = tk.Label(frame, text="Amount sold", 
                            font=('Arial', 20,"bold"), bg=BG_COLOR)
    amount_label.place(x=60, y=50)

    # entries
    num_entry = tk.Entry(frame, font=('Arial', 15,"bold"), bg=BUTTONS)
    num_entry.place(x=40, y=150, height=40)

    # combo box data
    options = main.combo_data("name", "Products")

    # create the combo box
    combo = ttk.Combobox(frame, values=options, font=('Arial', 15))
    combo.place(x=300, y=150, height=40)

    # Bind key release to the search function
    combo.bind('<KeyRelease>', lambda event: main.on_type(event, combo,
                                                          options))
    combo.bind('<Return>', lambda event: main.validate(event, num_entry,
                                                       combo, options, 2))
    num_entry.bind('<Return>', lambda event: main.validate(event, num_entry,
                                                           combo, options, 2))

    # buttons
    Save_changes =  tk.Button(frame, text="Save changes", cursor="hand2", 
                              font=('Arial', 17,"bold"), bg=BUTTONS, width=19,
                              height=3, highlightcolor=BLACK, bd=1, 
                              relief="solid", command=lambda event=None: 
                              main.validate(event, num_entry, combo, options,
                                            2))
    Save_changes.place(x=590, y=25)

def inventory_management(frame):
    """All the buttons and labels for the mang_frame"""
    # page selector frame
    page_frame = tk.Frame(master=frame, bg="#ffffff")
    page_frame.place(x=20, y=15, width=825, height=150)
    
    # frames
    sold_frame = tk.Frame(master=frame, bg=BG_COLOR)
    sold_frame.place(x=0, y=180, width=870, height=300)
    stock_sold(sold_frame)
    purchase_frame = tk.Frame(master=frame, bg=BG_COLOR)
    purchase_frame.place(x=0, y=180, width=870, height=300)
    product_purchase(purchase_frame)
    remove_frame = tk.Frame(master=frame, bg=BG_COLOR)
    remove_frame.place(x=0, y=180, width=870, height=300)
    remove_product(remove_frame)
    add_frame = tk.Frame(master=frame, bg=BG_COLOR)
    add_frame.place(x=0, y=180, width=870, height=300)
    add_product(add_frame)

    # page buttons for page selector
    sold = tk.Button(page_frame, text="Stock Sold", cursor="hand2", 
                     font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=13, 
                     height=4, highlightcolor=BLACK, bd=1, relief="solid", 
                     command=lambda: main.show_frame(None, sold_frame, "no"))
    sold.place(x=5, y=15)
    purchase = tk.Button(page_frame, text="Stock purchase", cursor="hand2", 
                         font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=13, 
                         height=4, highlightcolor=BLACK, bd=1, relief="solid",
                         command=lambda: main.show_frame(None, purchase_frame,
                                                         "no"))
    purchase.place(x=210, y=15)
    remove = tk.Button(page_frame, text="Remove a \nproduct", cursor="hand2", 
                       font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=13, 
                       height=4, highlightcolor=BLACK, bd=1, relief="solid",
                       command=lambda: main.show_frame(None, remove_frame,
                                                       "no"))
    remove.place(x=420, y=15)
    add = tk.Button(page_frame, text="add a product", cursor="hand2", 
                    font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=13, 
                    height=4, highlightcolor=BLACK, bd=1, relief="solid",
                    command=lambda: main.show_frame(None, add_frame, "no"))
    add.place(x=630, y=15)
