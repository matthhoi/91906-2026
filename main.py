"""This is a Python program that will be for owners of small shops. It will 
connect with a database and allow staff to complete inventory count, generate 
reports, and add new stock or remove old stock
By: Matt Smith                                                    00/00/2026"""

import tkinter as tk
from tkinter import messagebox
import sqlite3

# constants
DATABASE = "91906-2026\91906-database.db"
BG_COLOR = "#cccccc"
LABEL_COLOR = "#efefef"
WHITE = "#ffffff"
BLACK = "#000000"

# global variables
exit = False
login = False
is_visable = "*"
Show_Password_txt = "Show Password"

def show_password(password_entry):
    """show and hide the password"""
    global is_visable, Show_Password_txt
    # toggle the visibility of the password entry field
    if is_visable == "*":
        is_visable = ""
        password_entry.config(show=is_visable)
        Show_Password_txt = "Hide Password"
    else:
        is_visable = "*"
        password_entry.config(show=is_visable)
        Show_Password_txt = "Show Password"

def check_login(username_entry, password_entry, window):
    """Check if the username and password are correct"""
    global login, staff_id, staff_name
    # connect to the database
    with sqlite3.connect(DATABASE) as d_b:
        
        # Check if the username and password are correct
        cursor = d_b.cursor()
        qrl = f"""SELECT name FROM Staff WHERE username = 
        "{username_entry.get()}" AND password = "{password_entry.get()}";"""
        cursor.execute(qrl)
        results = cursor.fetchall()
        if not results == []:
            messagebox.showinfo("Login", 
                                f"Login successful! \n Welcome {results[0][0]}")
            
            # get the staff id and name from the database
            qrl = f"""SELECT staff_id, name FROM Staff WHERE username = 
            "{username_entry.get()}" AND password = "{password_entry.get()}";"""
            cursor.execute(qrl)
            results = cursor.fetchall()
            staff_id = results[0][0]
            staff_name = results[0][1]

            # close the login window
            window.destroy()
            login = True
        else:
            messagebox.showerror("Login", "Invalid username or password.")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

def sign_in():
    """Sign in the user"""
    global login, exit, is_visable, Show_Password_txt
    login = False
    # login window
    while login == False:
        # Create the login window
        window = tk.Tk()
        window.title("Login Window")
        window.geometry("1000x650")
        window.config(bg=BG_COLOR)
        window.resizable(width=False, height=False)

        # Create the mian Frame
        frame = tk.Frame(master=window, bg=WHITE)
        frame.place(x=200, y=25, width=600, height=600)

        # Create the login feilds
        username_label = tk.Label(frame, text="Username", 
                                  font=('Arial',15,"bold"), bg=WHITE) 
        username_entry = tk.Entry(frame, width=75, bg=BG_COLOR, relief="flat", 
                                  highlightbackground=BLACK, highlightthickness=1)
        password_label = tk.Label(frame, text="Password", 
                                  font=('Arial',15,"bold"), bg=WHITE)
        password_entry = tk.Entry(frame, show=is_visable, width=75, bg=BG_COLOR, 
                                  relief="flat", highlightbackground=BLACK, 
                                  highlightthickness=1)
        username_entry.place(x=25, y=130)
        username_label.place(x=50, y=100)
        password_entry.place(x=25, y=230)
        password_label.place(x=50, y=200)

        # show password button
        show_password_b = tk.Button(frame, text=Show_Password_txt, cursor="hand2", 
                                  font=('Arial', 12), bg=LABEL_COLOR, 
                                  command=lambda password_entry=password_entry: 
                                  show_password(password_entry))
        show_password_b.place(x=350, y=300)

        # Create the login button
        login_button = tk.Button(frame, text="sign in", cursor="hand2",
                                 font=('Arial', 15,"bold"), bg=LABEL_COLOR, 
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

while __name__ == "__main__":
    """run the program"""
    # start the login process
    sign_in()
    
    break
