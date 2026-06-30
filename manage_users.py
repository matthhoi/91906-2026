"""This is a Python program that will be for owners of small shops. It will
connect with a database and allow staff to complete inventory count, generate
reports, and add new stock or remove old stock
By: Matt Smith                                                    30/06/2026"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import main

BUTTONS = "#C5C2D0"
BG_COLOR = "#cccccc"
LABEL_COLOR = "#efefef"
BLACK = "#000000"
PERMISSIONS = ["Admin", "Manager", "User"]

# manage users


def validate_add_user(event, combo, username, password, name):
    """validate the entries from add user and update the database"""
    # get hightest id
    result = main.connect_with_database("""SELECT MAX(staff_id) FROM Staff;""",
                                        1)

    # create new id
    if result[0][0] is None:
        staff_id = 1
    else:
        staff_id = result[0][0] + 1

    # cheek the entries
    if combo.get() in PERMISSIONS and not username.get() == "" and not \
            password.get() == "" and not name.get() == "":
        # update the database
        main.connect_with_database(f"""INSERT INTO Staff (staff_id, username,
                                   password, name, permissions) VALUES
                                   ({staff_id}, "{username.get()}",
                                   "{password.get()}", "{name.get()}",
                                   "{combo.get()}");""", 2)
        messagebox.showinfo("success", "successfully updated database")
        combo.delete(0, tk.END)
        username.delete(0, tk.END)
        password.delete(0, tk.END)
        name.delete(0, tk.END)
    else:
        messagebox.showerror("error", "entries cant be blank or permissions "
                             "has to be in options")


def validate_remove_user(event, combo, options):
    """validate the entries from remove user and update the database"""
    if combo.get() in options:
        main.connect_with_database(f"""DELETE FROM Staff WHERE name =
                                    "{combo.get()}";""", 2)
        messagebox.showinfo("success", "successfully updated database")
        combo.delete(0, tk.END)
    else:
        messagebox.showerror("error", "name has to be in options")


def add_remove_users(frame):
    """"All the buttons and labels add/remove a user in user_frame"""
    # labels
    Select_label = tk.Label(frame, text="Select user",
                            font=('Arial', 20, "bold"), bg=BG_COLOR)
    Select_label.place(x=80, y=30)
    username_label = tk.Label(frame, text="username",
                              font=('Arial', 15, "bold"), bg=BG_COLOR)
    username_label.place(x=355, y=20)
    password_label = tk.Label(frame, text="password",
                              font=('Arial', 15, "bold"), bg=BG_COLOR)
    password_label.place(x=355, y=90)
    name_label = tk.Label(frame, text="Name", font=('Arial', 15, "bold"),
                          bg=BG_COLOR)
    name_label.place(x=370, y=160)
    permissions_label = tk.Label(frame, text="permissions",
                                 font=('Arial', 15, "bold"), bg=BG_COLOR)
    permissions_label.place(x=337, y=230)
    # entries
    username_entry = tk.Entry(frame, font=('Arial', 15, "bold"), bg=BUTTONS)
    username_entry.place(x=470, y=15, height=40)
    password_entry = tk.Entry(frame, font=('Arial', 15, "bold"), bg=BUTTONS)
    password_entry.place(x=470, y=88, height=40)
    name_entry = tk.Entry(frame, font=('Arial', 15, "bold"), bg=BUTTONS)
    name_entry.place(x=470, y=155, height=40)

    # combos
    # combo box data
    user_options = main.combo_data("name", "Staff")

    # create the combo box
    user_combo = ttk.Combobox(frame, values=user_options, font=('Arial', 15))
    user_combo.place(x=40, y=120, height=40)
    position_combo = ttk.Combobox(frame, values=PERMISSIONS,
                                  font=('Arial', 15))
    position_combo.place(x=470, y=225, height=40, width=225)

    # Bind key release to the search function
    user_combo.bind('<KeyRelease>', lambda event: main.on_type(event,
                    user_combo, user_options))
    user_combo.bind('<Return>', lambda event: validate_remove_user(event,
                    user_combo, user_options))
    position_combo.bind('<Return>', lambda event: validate_add_user(event,
                        position_combo, username_entry, password_entry,
                        name_entry))
    username_entry.bind('<Return>', lambda event: validate_add_user(event,
                        position_combo, username_entry, password_entry,
                        name_entry))
    password_entry.bind('<Return>', lambda event: validate_add_user(event,
                        position_combo, username_entry, password_entry,
                        name_entry))
    name_entry.bind('<Return>', lambda event: validate_add_user(event,
                    position_combo, username_entry, password_entry,
                    name_entry))

    # buttons
    save_changes = tk.Button(frame, text="Save\nchanges", cursor="hand2",
                             font=('Arial', 15, "bold"), bg=BUTTONS, width=12,
                             height=2, highlightcolor=BLACK, bd=1,
                             relief="solid", command=lambda event=None:
                             validate_add_user(event, position_combo,
                                               username_entry, password_entry,
                                               name_entry))
    save_changes.place(x=710, y=210)
    remove_user = tk.Button(frame, text="remove user", cursor="hand2",
                            font=('Arial', 18, "bold"), bg=BUTTONS, width=14,
                            height=2, highlightcolor=BLACK, bd=1,
                            relief="solid", command=lambda event=None:
                            validate_remove_user(event, user_combo,
                                                 user_options))
    remove_user.place(x=55, y=200)


def validate_password(event, combo, options, password_entry):
    """validate the entries from change password and update the database"""
    if combo.get() in options and not password_entry.get() == "":
        main.save_changes("staff", "password", password_entry.get(), "name",
                          combo.get())
        messagebox.showinfo("success", "successfully updated database")
        combo.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("error", "name or new permissions has to be in "
                             "options")


def change_password(frame):
    """All the buttons and labels changing the password of a user in
    user_frame"""

    # labels
    Select_label = tk.Label(frame, text="Select user",
                            font=('Arial', 20, "bold"), bg=BG_COLOR)
    Select_label.place(x=360, y=70)
    permissions_label = tk.Label(frame, text="password",
                                 font=('Arial', 20, "bold"), bg=BG_COLOR)
    permissions_label.place(x=100, y=70)

    # combo box data
    options = main.combo_data("name", "Staff")

    # create the combo box
    combo = ttk.Combobox(frame, values=options, font=('Arial', 15))
    combo.place(x=320, y=150, height=40)

    # entries
    password_entry = tk.Entry(frame, font=('Arial', 20, "bold"), bg=BUTTONS)
    password_entry.place(x=10, y=150, height=40)

    # Bind key release to the search function
    combo.bind('<KeyRelease>', lambda event: main.on_type(event, combo,
                                                          options))
    combo.bind('<Return>', lambda event: validate_password(event, combo,
               options, password_entry))
    password_entry.bind('<Return>', lambda event: validate_password(event,
                        combo, options, password_entry))

    # buttons
    Save_changes = tk.Button(frame, text="Save changes", cursor="hand2",
                             font=('Arial', 17, "bold"), bg=BUTTONS, width=18,
                             height=3, highlightcolor=BLACK, bd=1,
                             relief="solid", command=lambda event=None:
                             validate_password(event, combo, options,
                                               password_entry))
    Save_changes.place(x=590, y=25)


def validate_permissions(event, user_combo, options, permission_combo):
    """validate the entries from change permissions and update the database"""
    # validate entries
    if user_combo.get() in options and permission_combo.get() in PERMISSIONS:
        main.save_changes("staff", "permissions", permission_combo.get(),
                          "name", user_combo.get())
        messagebox.showinfo("success", "successfully updated database")
        user_combo.delete(0, tk.END)
        permission_combo.delete(0, tk.END)
    else:
        messagebox.showerror("error", "name or new permissions has to be in "
                             "options")


def change_permissions(frame):
    """"All the buttons and labels changing the permissions of a user in
    user_frame"""

    # labels
    Select_label = tk.Label(frame, text="Select user",
                            font=('Arial', 20, "bold"), bg=BG_COLOR)
    Select_label.place(x=340, y=70)
    permissions_label = tk.Label(frame, text="New\npermissions",
                                 font=('Arial', 20, "bold"), bg=BG_COLOR)
    permissions_label.place(x=40, y=50)

    # combo box data
    options = main.combo_data("name", "Staff")

    # create the combo box
    user_combo = ttk.Combobox(frame, values=options, font=('Arial', 15))
    user_combo.place(x=300, y=150, height=40)

    # Bind key release to the search function
    user_combo.bind('<KeyRelease>', lambda event: main.on_type(event,
                    user_combo, options))

    # create the combo box
    permission_combo = ttk.Combobox(frame, values=PERMISSIONS,
                                    font=('Arial', 15))
    permission_combo.place(x=10, y=150, height=40)

    user_combo.bind('<Return>', lambda event: validate_permissions(event,
                    user_combo, options, permission_combo))
    permission_combo.bind('<Return>', lambda event: validate_permissions(event,
                          user_combo, options, permission_combo))

    # buttons
    Save_changes = tk.Button(frame, text="Save changes", cursor="hand2",
                             font=('Arial', 17, "bold"), bg=BUTTONS, width=19,
                             height=3, highlightcolor=BLACK, bd=1,
                             relief="solid", command=lambda event=None:
                             validate_permissions(event, user_combo, options,
                                                  permission_combo))
    Save_changes.place(x=590, y=25)


def manage_users(frame):
    """All the buttons and labels for the users_frame"""
    # page selector frame
    page_frame = tk.Frame(master=frame, bg="#ffffff")
    page_frame.place(x=20, y=15, width=825, height=150)

    # frames
    permissions_frame = tk.Frame(master=frame, bg=BG_COLOR)
    permissions_frame.place(x=0, y=180, width=870, height=300)
    change_permissions(permissions_frame)
    password_frame = tk.Frame(master=frame, bg=BG_COLOR)
    password_frame.place(x=0, y=180, width=870, height=300)
    change_password(password_frame)
    add_user_frame = tk.Frame(master=frame, bg=BG_COLOR)
    add_user_frame.place(x=0, y=180, width=870, height=300)
    add_remove_users(add_user_frame)

    # page buttons for page selector
    permissions = tk.Button(page_frame, text="Change\npermissions",
                            cursor="hand2", font=('Arial', 17, "bold"),
                            bg=LABEL_COLOR, width=15, height=4,
                            highlightcolor=BLACK, bd=1, relief="solid",
                            command=lambda: main.show_frame
                            (None, permissions_frame, "no"))
    permissions.place(x=5, y=15)
    password = tk.Button(page_frame, text="Change\npassword", cursor="hand2",
                         font=('Arial', 17, "bold"), bg=LABEL_COLOR, width=15,
                         height=4, highlightcolor=BLACK, bd=1, relief="solid",
                         command=lambda: main.show_frame
                         (None, password_frame, "no"))
    password.place(x=300, y=15)
    add_user = tk.Button(page_frame, text="Create/Remove\nuser",
                         cursor="hand2", font=('Arial', 17, "bold"),
                         bg=LABEL_COLOR, width=15, height=4,
                         highlightcolor=BLACK, bd=1, relief="solid",
                         command=lambda: main.show_frame
                         (None, add_user_frame, "no"))
    add_user.place(x=600, y=15)
