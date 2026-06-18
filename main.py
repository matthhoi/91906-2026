"""This is a Python program that will be for owners of small shops. It will
connect with a database and allow staff to complete inventory count, generate
reports, and add new stock or remove old stock
By: Matt Smith                                                    00/00/2026"""

import tkinter as tk
from tkinter import messagebox
import sqlite3
import report
import products
from tkinter import ttk

# constants
DATABASE = "91906-2026\91906-database.db"
BUTTONS = "#C5C2D0"
BG_COLOR = "#cccccc"
LABEL_COLOR = "#efefef"
WHITE = "#ffffff"
BLACK = "#000000"

# global variables
exit = False
login = False
is_visible = "*"
Show_Password_txt = "Show Password"
staff_position = "Admin"
staff_name = ""
order_list = []
total_price = 0.0
inventory_list = []

# functions
def save_changes(table, column, data, where, thing):
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        qrl = f"""UPDATE {table} SET {column} = "{data}" WHERE {where} 
        = "{thing}";"""
        cursor.execute(qrl)

def show_frame(window_main, frame, text):
    """Brings the frame to the front and chantages the title"""
    if text == "no":
        pass
    else:
        window_main.title(text)
    frame.tkraise()

def permissions(window_main, frame, button):
    """Check the users permissions"""
    global staff_position
    # check if the user has the admin permissions
    if button == "manage users":
        if staff_position == "Admin":
            show_frame(window_main, frame, "manage users")
        else:
            messagebox.showerror("Error", "You don't have the correct "
                                 "permissions")
    # check if the user has the admin or manager permissions
    elif button == "Inventory management":
        if staff_position == "Manager" or staff_position == "Admin":
            show_frame(window_main, frame, "Inventory management")
        else:
            messagebox.showerror("Error", "You don't have the correct "
                                 "permissions")

def validate(num_entry, combo, options, where):
    """validate the entries"""
    # validate entries
    if num_entry.isdigit() and combo in options:
        if where == 1:
            save_changes("Products", "count", num_entry, "name", combo)
            messagebox.showinfo("success", "successfully updated database")
        elif where == 2:
            save_changes("Products", "sold", num_entry, "name", combo)
            messagebox.showinfo("success", "successfully updated database")
    else:
        messagebox.showerror("error", "Number of products has to be a number "
                             "and or product has to be selected")

def combo_data():
    """Get the data for the combo box from the database"""
    # connect with the database and get data
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        qrl = f"""SELECT name from products;"""
        cursor.execute(qrl)
        results = cursor.fetchall()

    # get the data into options
    options = []
    for x in range(0, len(results)):
        options.append(results[x][0])
    return options

def on_type(event, combo, options):
    """sorts the data in options"""
    # Get current text from the combobox
    typed_text = combo.get()
    
    if typed_text == '':
        # Reset to full list if search is empty
        combo['values'] = options
    else:
        # Filter list based on typed characters (case-insensitive)
        filtered_data = [item for item in options if typed_text.lower() in 
                         item.lower()]
        combo['values'] = filtered_data

# manage users
def manage_users(frame):
    """All the buttons and labels for the users_frame"""
        # page selector frame
    page_frame = tk.Frame(master=frame, bg=WHITE)
    page_frame.place(x=20, y=15, width=825, height=150)
    
    # frames
    permissions_frame = tk.Frame(master=frame, bg=BG_COLOR)
    permissions_frame.place(x=0, y=180, width=870, height=300)
    change_permissions(permissions_frame)
    password_frame = tk.Frame(master=frame, bg=BG_COLOR)
    password_frame.place(x=0, y=180, width=870, height=300)
    (password_frame)
    add_user_frame = tk.Frame(master=frame, bg=BG_COLOR)
    add_user_frame.place(x=0, y=180, width=870, height=300)
    (add_user_frame)

    # page buttons for page selector
    permissions = tk.Button(page_frame, text="Change\npermissions",
                            cursor="hand2", font=('Arial', 17,"bold"),
                            bg=LABEL_COLOR, width=15, height=4,
                            highlightcolor=BLACK, bd=1, relief="solid",
                            command=lambda: show_frame
                            (None, permissions_frame, "no"))
    permissions.place(x=5, y=15)
    password = tk.Button(page_frame, text="Change\npassword", cursor="hand2",
                         font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=15,
                         height=4, highlightcolor=BLACK, bd=1, relief="solid",
                         command=lambda: show_frame
                         (None, password_frame, "no"))
    password.place(x=300, y=15)
    add_user = tk.Button(page_frame, text="Create/Remove\nuser", 
                         cursor="hand2", font=('Arial', 17,"bold"),
                         bg=LABEL_COLOR, width=15, height=4,
                         highlightcolor=BLACK, bd=1, relief="solid",
                         command=lambda: show_frame
                         (None, add_user_frame, "no"))
    add_user.place(x=600, y=15)

# inventory management
def add(barcode, name, type, cost, amount, display):
    """validate the entries and update the database"""

    # see is barcode is already in the database
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        qrl = f"""SELECT barcode FROM products WHERE barcode = 
        "{barcode.get()}";"""
        cursor.execute(qrl)
        results = cursor.fetchall()
        if results == []:
            ask = True
        else:
            # ask if the user wishes to change the current entry
            ask = messagebox.askyesno("Warning", "This barcode already " \
            "exists do you want to override this entry")
            if ask == True:
                with sqlite3.connect(DATABASE) as d_b:
                    cursor = d_b.cursor()
                    qrl = f"""DELETE FROM Products WHERE barcode = 
                    "{barcode.get()}";"""
                    cursor.execute(qrl)
    
    # see if any of the entries are empty
    if name.get() == "" or type.get() == "" or display.get() == "":
        messagebox.showerror("error", "Entries can not be blank")
    else:
        try:
            # see if any of the barcode, cost, and amount are numbers
            if ask == True and barcode.get().isdigit() and float(cost.get()) \
                and amount.get().isdigit():
                # create a new entry and delete the entries
                with sqlite3.connect(DATABASE) as d_b:
                    cursor = d_b.cursor()
                    qrl = f"""INSERT INTO products (barcode, name, type, cost, 
                    amount, display_name) VALUES ({barcode.get()}, 
                    "{name.get()}", "{type.get()}", {cost.get()}, 
                    {amount.get()}, "{display.get()}");"""
                    cursor.execute(qrl)
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
        except Exception as e:
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

    # buttons
    update =  tk.Button(frame, text="Save\nchanges", cursor="hand2",
                        font=('Arial', 15,"bold"), bg=BUTTONS, width=12,
                        height=2, highlightcolor=BLACK, bd=1, relief="solid",
                        command=lambda: add(barcode_entry, name_entry, 
                        type_entry, cost_entry, amount_entry, display_entry))
    update.place(x=710, y=210)

def remove(combo, options):
    """validate the entries and update the database"""
        # validate entries
    if combo in options:
        yes_no = messagebox.askyesno("warning", "This action can NOT be "
                                     "undone are you sure?")
        if yes_no == True:
            with sqlite3.connect(DATABASE) as d_b:
                cursor = d_b.cursor()
                qrl = f"""DELETE FROM Products WHERE name = "{combo}";"""
                cursor.execute(qrl)
            messagebox.showinfo("success", "successfully updated database")
    else:
        messagebox.showerror("error", "product has to be in options")

def remove_product(frame):
    """All the buttons and labels for remove product in mang_frame"""
    
    # combo box data
    options = combo_data()

    # create the combo box
    combo = ttk.Combobox(frame, values=options, font=('Arial', 15))
    combo.place(x=300, y=200, height=40)

    # Bind key release to the search function
    combo.bind('<KeyRelease>', lambda event: on_type(event, combo, options))

    # buttons
    update =  tk.Button(frame, text="remove product", cursor="hand2",
                        font=('Arial', 17,"bold"), bg=BUTTONS, width=19,
                        height=3, highlightcolor=BLACK, bd=1, relief="solid",
                        command=lambda: remove(combo.get(), options))
    update.place(x=290, y=25)

def purchase(num_entry, combo, options, cost_entry):
    """validate the entries and get the data need to update the database"""
    # validate entries
    if num_entry.get().isdigit() and combo.get() in options and \
        float(cost_entry.get()):
        if float(cost_entry.get()) > 0:
            with sqlite3.connect(DATABASE) as d_b:
                cursor = d_b.cursor()
                qrl = f"""SELECT cost, amount, purchase FROM Products WHERE 
                name = "{combo.get()}";"""
                cursor.execute(qrl)
                results = cursor.fetchall()
                current_total_value = results[0][1] * results[0][0]
                new_total_value = int(num_entry.get()) * float(cost_entry.get())
                total_quantity = results[0][2] + int(num_entry.get())
                total_value = current_total_value + new_total_value
                new_cost = total_value / total_quantity
                save_changes("Products", "cost", new_cost, "name", combo.get())
                save_changes("Products", "purchase", total_quantity, "name", \
                    combo.get())
                num_entry.delete(0, tk.END)
                combo.delete(0, tk.END)
                cost_entry.delete(0, tk.END)
                messagebox.showinfo("success", "successfully updated database")
        else:
            messagebox.showerror("error", "cost has to be a positive number")
    else:
        messagebox.showerror("error", "Number of products has to be a number "
                             "and or product has to be selected")

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
    options = combo_data()

    # create the combo box
    combo = ttk.Combobox(frame, values=options, font=('Arial', 15))
    combo.place(x=600, y=200, height=40)

    # Bind key release to the search function
    combo.bind('<KeyRelease>', lambda event: on_type(event, combo, options))

    # buttons
    save_changes =  tk.Button(frame, text="Save changes", cursor="hand2", 
                              font=('Arial', 17,"bold"), bg=BUTTONS, width=19,
                              height=3, highlightcolor=BLACK, bd=1, 
                              relief="solid", command=lambda: purchase
                              (num_entry, combo, options, 
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
    options = combo_data()

    # create the combo box
    combo = ttk.Combobox(frame, values=options, font=('Arial', 15))
    combo.place(x=300, y=150, height=40)

    # Bind key release to the search function
    combo.bind('<KeyRelease>', lambda event: on_type(event, combo, options))

    # buttons
    Save_changes =  tk.Button(frame, text="Save changes", cursor="hand2", 
                              font=('Arial', 17,"bold"), bg=BUTTONS, width=19,
                              height=3, highlightcolor=BLACK, bd=1, 
                              relief="solid", command=lambda: validate
                              (num_entry.get(), combo.get(), options, 2))
    Save_changes.place(x=590, y=25)

def inventory_management(frame):
    """All the buttons and labels for the mang_frame"""
    # page selector frame
    page_frame = tk.Frame(master=frame, bg=WHITE)
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
                     command=lambda: show_frame(None, sold_frame, "no"))
    sold.place(x=5, y=15)
    purchase = tk.Button(page_frame, text="Stock purchase", cursor="hand2", 
                         font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=13, 
                         height=4, highlightcolor=BLACK, bd=1, relief="solid",
                         command=lambda: show_frame(None, purchase_frame, "no"))
    purchase.place(x=210, y=15)
    remove = tk.Button(page_frame, text="Remove a \nproduct", cursor="hand2", 
                       font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=13, 
                       height=4, highlightcolor=BLACK, bd=1, relief="solid",
                       command=lambda: show_frame(None, remove_frame, "no"))
    remove.place(x=420, y=15)
    add = tk.Button(page_frame, text="add a product", cursor="hand2", 
                    font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=13, 
                    height=4, highlightcolor=BLACK, bd=1, relief="solid",
                    command=lambda: show_frame(None, add_frame, "no"))
    add.place(x=630, y=15)

# inventory count
def make_report():
    """get all the info from the database and add that info to the report"""
    global staff_name, inventory_list
    # connect with the database and get the products info
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        qrl = f"""SELECT * from products;"""
        cursor.execute(qrl)
        results = cursor.fetchall()
        # put the results into the products .py function
        for x in range(0, len(results)):
            product = products.products(results[x][0], results[x][8], 
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
    options = combo_data()

    # create the combo box
    combo = ttk.Combobox(frame, values=options, font=('Arial', 15))
    combo.place(x=30, y=150, height=40)

    # Bind key release to the search function
    combo.bind('<KeyRelease>', lambda event: on_type(event, combo, options))
    # buttons
    gen_report =  tk.Button(frame, text="Generate report", cursor="hand2", 
                            font=('Arial', 17,"bold"), bg=BUTTONS, width=19,
                            height=3, highlightcolor=BLACK, bd=1, 
                            relief="solid", command=lambda: make_report())
    gen_report.place(x=590, y=350)
    Save_changes =  tk.Button(frame, text="Save changes", cursor="hand2", 
                            font=('Arial', 17,"bold"), bg=BUTTONS, width=19,
                            height=3, highlightcolor=BLACK, bd=1, 
                            relief="solid", command=lambda: validate
                            (num_entry.get(), combo.get(), options, 1))
    Save_changes.place(x=590, y=25)

# main
def main_window():
    """Create the main window and call the other layers"""
    global exit
    while exit == False:
        # Create the main menu window
        window_main = tk.Tk()
        window_main.title("main window")
        window_main.geometry("900x650")
        window_main.config(bg=BG_COLOR)
        window_main.resizable(width=False, height=False)

        # frames
        # page selector
        win_frame = tk.Frame(master=window_main, bg=WHITE)
        win_frame.place(x=15, y=15, width=870, height=125)

        # manage users
        users_frame = tk.Frame(master=window_main, bg=BG_COLOR)
        users_frame.place(x=15, y=150, width=870, height=480)
        manage_users(users_frame)

        # inventory management
        mang_frame = tk.Frame(master=window_main, bg=BG_COLOR)
        mang_frame.place(x=15, y=150, width=870, height=480)
        inventory_management(mang_frame)

        # inventory count
        count_frame = tk.Frame(master=window_main, bg=BG_COLOR)
        count_frame.place(x=15, y=150, width=870, height=480)
        inventory_count(count_frame)

        # page buttons for page selector
        users = tk.Button(win_frame, text="manage users", cursor="hand2", 
                          font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=19, 
                          height=3, highlightcolor=BLACK, bd=1, relief="solid", 
                          command=lambda: permissions(window_main, users_frame, 
                                                     "manage users"))
        users.place(x=5, y=15)
        mang = tk.Button(win_frame, text="Inventory management", cursor="hand2", 
                         font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=19, 
                         height=3, highlightcolor=BLACK, bd=1, relief="solid", 
                         command=lambda: permissions(window_main, mang_frame, 
                                                     "Inventory management"))
        mang.place(x=300, y=15)
        count = tk.Button(win_frame, text="Inventory count", cursor="hand2", 
                          font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=19, 
                          height=3, highlightcolor=BLACK, bd=1, relief="solid", 
                          command=lambda: show_frame(window_main, count_frame, 
                                                     "Inventory count"))
        count.place(x=590, y=15)

        window_main.mainloop()

        if exit == False:
                # exit the program if the user clicks the exit button
                exit = messagebox.askokcancel("Exit", 
                "Are you sure you want to exit?")
        else:
            # exit the program if the user clicks the exit button
            break

# login
def show_password(password_entry):
    """show and hide the password"""
    global is_visible, Show_Password_txt
    # toggle the visibility of the password entry field
    if is_visible == "*":
        is_visible = ""
        password_entry.config(show=is_visible)
        Show_Password_txt = "Hide Password"
    else:
        is_visible = "*"
        password_entry.config(show=is_visible)
        Show_Password_txt = "Show Password"

def check_login(username_entry, password_entry, window):
    """Check if the username and password are correct"""
    global login, staff_position, staff_name
    # connect to the database
    with sqlite3.connect(DATABASE) as d_b:
        
        # Check if the username and password are correct
        cursor = d_b.cursor()
        qrl = f"""SELECT name FROM Staff WHERE username = 
        "{username_entry.get()}" AND password = "{password_entry.get()}";"""
        cursor.execute(qrl)
        results = cursor.fetchall()
        if not results == []:
            messagebox.showinfo("Login", "Login successful! \n Welcome "
                                f"{results[0][0]}")
            staff_name = results[0][0]

            # get the position from the database
            qrl = f"""SELECT permissions FROM Staff WHERE username = 
            "{username_entry.get()}";"""
            cursor.execute(qrl)
            results = cursor.fetchall()
            staff_position = results[0][0]

            # close the login window
            window.destroy()
            login = True
        else:
            messagebox.showerror("Login", "Invalid username or password.")
            password_entry.delete(0, tk.END)

def sign_in():
    """Sign in the user"""
    global login, exit, is_visible, Show_Password_txt
    login = False
    # login window
    while login == False:
        # Create the login window
        window = tk.Tk()
        window.title("Login Window")
        window.geometry("1000x650")
        window.config(bg=BG_COLOR)
        window.resizable(width=False, height=False)

        # Create the main Frame
        frame = tk.Frame(master=window, bg=WHITE)
        frame.place(x=200, y=75, width=600, height=500)

        # text
        text = tk.Label(frame, text="login", font=('Arial',25,"bold"), 
                        bg=WHITE)
        text.place(x=250, y=15)
        
        # Create the login fields
        username_label = tk.Label(frame, text="Username", 
                                  font=('Arial',15,"bold"), bg=WHITE) 
        username_entry = tk.Entry(frame, width=75, bg=BG_COLOR, relief="flat", 
                                  highlightbackground=BLACK, 
                                  highlightthickness=1)
        password_label = tk.Label(frame, text="Password", 
                                  font=('Arial',15,"bold"), bg=WHITE)
        password_entry = tk.Entry(frame, show=is_visible, width=75, 
                                  bg=BG_COLOR, relief="flat", 
                                  highlightbackground=BLACK, 
                                  highlightthickness=1)
        username_entry.place(x=25, y=130)
        username_label.place(x=50, y=100)
        password_entry.place(x=25, y=230)
        password_label.place(x=50, y=200)

        # show password button
        show_password_b = tk.Button(frame, text=Show_Password_txt, 
                                    cursor="hand2", font=('Arial', 12), 
                                    bg=LABEL_COLOR, highlightcolor=BLACK, 
                                    bd=1, relief="solid", command=lambda 
                                    password_entry=password_entry: 
                                    show_password(password_entry))
        show_password_b.place(x=350, y=300)

        # Create the login button
        login_button = tk.Button(frame, text="sign in", cursor="hand2",
                                 font=('Arial', 15,"bold"), bg=LABEL_COLOR, 
                                 highlightcolor=BLACK, bd=1, relief="solid", 
                                 width=10, height=2, command=lambda 
                                 username_entry=username_entry, 
                                 password_entry=password_entry, window=window:
                                 check_login(username_entry, password_entry, 
                                             window))
        login_button.place(x=225, y=400)
        window.mainloop()

        if login == False:
            # exit the program if the user clicks the exit button
            exit = messagebox.askokcancel("Exit", 
            "Are you sure you want to exit?")
            login = exit
        
    while True:
        if exit == True:
            break
        global order_id, order_no
        # run rest of program
        main_window()

while __name__ == "__main__":
    """run the program"""
    # start the login process
    main_window()
    
    break
