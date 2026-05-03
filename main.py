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
staff_position = ""
staff_name = ""

# funtions
def show_frame(window_main, frame, text):
    """Brings the frame to the front and chnmages the title"""
    window_main.title(text)
    frame.tkraise()

def main_window():
    """Create the main window and call the other layers"""
    global exit, title
    while exit == False:
        # Create the mian menu window
        window_main = tk.Tk()
        window_main.title("main window")
        window_main.geometry("900x650")
        window_main.config(bg=BG_COLOR)
        window_main.resizable(width=False, height=False)

        # frames
        # page selcetor
        win_frame = tk.Frame(master=window_main,bg=WHITE)
        win_frame.place(x=15,y=15,width=870,height=125)
        # magege users
        users_frame = tk.Frame(master=window_main,bg=BG_COLOR)
        users_frame.place(x=15,y=150,width=870,height=480)
        # inventory management
        mang_frame = tk.Frame(master=window_main,bg=BG_COLOR)
        mang_frame.place(x=15,y=150,width=870,height=480)
        # inventory count
        count_frame = tk.Frame(master=window_main,bg=BG_COLOR)
        count_frame.place(x=15,y=150,width=870,height=480)

        # page buttons for page selcetor
        users = tk.Button(win_frame, text="Manage users", cursor="hand2", 
                          font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=19, 
                          height=3, highlightcolor=BLACK, bd=1, relief="solid", 
                          command=lambda: show_frame(window_main, users_frame, 
                                                     "Manage users"))
        users.place(x=5, y=15)
        mang = tk.Button(win_frame, text="Inventory management", cursor="hand2", 
                          font=('Arial', 17,"bold"), bg=LABEL_COLOR, width=19, 
                          height=3, highlightcolor=BLACK, bd=1, relief="solid", 
                          command=lambda: show_frame(window_main, mang_frame, 
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
            messagebox.showinfo("Login", 
                                f"Login successful! \n Welcome {results[0][0]}")
            staff_name = results[0][0]

            # get the position from the database
            qrl = f"""SELECT position FROM Staff WHERE username = 
            "{username_entry.get()}";"""
            cursor.execute(qrl)
            results = cursor.fetchall()
            staff_position = results[0][0]

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
        frame.place(x=200, y=75, width=600, height=500)

        # text
        text = tk.Label(frame, text="login", font=('Arial',25,"bold"), bg=WHITE)
        text.place(x=250, y=15)
        
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
                                  highlightcolor=BLACK, bd=1, relief="solid", 
                                  command=lambda password_entry=password_entry: 
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
