"""This is a Python program that will be for owners of small shops. It will
connect with a database and allow staff to complete inventory count, generate
reports, and add new stock or remove old stock
By: Matt Smith                                                    26/06/2026"""

import tkinter as tk
from tkinter import messagebox
import sqlite3
import manage_users
import inventory_count
import inventory_management

# constants
DATABASE = "91906-2026\91906-database.db"
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

# functions
def connect_with_database(qrl, res):
    """connect with the database"""
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        cursor.execute(qrl)
        # return results or not
        if res == 1:
            results = cursor.fetchall()
            return results

def save_changes(table, column, data, where, thing):
    """default save database update"""
    connect_with_database(f"""UPDATE {table} SET {column} = "{data}" WHERE 
                          {where} = "{thing}";""", 2)

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

def validate(event, num_entry, combo, options, where):
    """validate the entries"""
    # validate entries
    try:
        if num_entry.get().isdigit() and combo.get() in options:
            if where == 1:
                save_changes("Products", "count", num_entry.get(), "name",
                combo.get())
                messagebox.showinfo("success", "successfully updated database")
            elif where == 2:
                save_changes("Products", "sold", num_entry.get(), "name",
                combo.get())
                messagebox.showinfo("success", "successfully updated database")
            num_entry.delete(0, tk.END)
            combo.delete(0, tk.END)
        else:
            messagebox.showerror("error", "Number of products has to be a "
            "number and or product has to be selected")
    except:
        messagebox.showerror("error", f"cost has to be a number")

def combo_data(column, table):
    """Get the data for the combo box from the database"""
    # connect with the database and get data
    results = connect_with_database(f"""SELECT {column} from {table};""", 1)

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
        manage_users.manage_users(users_frame)

        # inventory management
        mang_frame = tk.Frame(master=window_main, bg=BG_COLOR)
        mang_frame.place(x=15, y=150, width=870, height=480)
        inventory_management.inventory_management(mang_frame)
        
        # inventory count
        count_frame = tk.Frame(master=window_main, bg=BG_COLOR)
        count_frame.place(x=15, y=150, width=870, height=480)
        inventory_count.inventory_count(count_frame)

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

def check_login(event, username_entry, password_entry, window):
    """Check if the username and password are correct"""
    global login, staff_position, staff_name
    # connect to the database
    results = connect_with_database(f"""SELECT name FROM Staff WHERE username 
                                    = "{username_entry.get()}" AND password = 
                                    "{password_entry.get()}";""", 1)
    # Check if the username and password are correct
    if not results == []:
        messagebox.showinfo("Login", "Login successful! \n Welcome "
                            f"{results[0][0]}")
        staff_name = results[0][0]

        # get the position from the database
        results = connect_with_database(f"""SELECT permissions FROM Staff 
                                        WHERE username = 
                                        "{username_entry.get()}";""", 1)
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
                                    bd=1, relief="solid", command=lambda: 
                                    show_password(password_entry))
        show_password_b.place(x=350, y=300)

        # Create the login button
        login_button = tk.Button(frame, text="sign in", cursor="hand2",
                                 font=('Arial', 15,"bold"), bg=LABEL_COLOR, 
                                 highlightcolor=BLACK, bd=1, relief="solid", 
                                 width=10, height=2, command=lambda event=None: 
                                 check_login(event, username_entry, 
                                 password_entry, window))
        login_button.place(x=225, y=400)

        password_entry.bind('<Return>', lambda event: check_login(event, 
                            username_entry, password_entry, window))
        username_entry.bind('<Return>', lambda event: check_login(event, 
                            username_entry, password_entry, window))

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
