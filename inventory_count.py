"""This is a Python program that will be for owners of small shops. It will
connect with a database and allow staff to complete inventory count, generate
reports, and add new stock or remove old stock
By: Matt Smith                                                    26/06/2026"""

import tkinter as tk
from tkinter import ttk
import main

BUTTONS = "#C5C2D0"
BG_COLOR = "#cccccc"
BLACK = "#000000"

# inventory count



def inventory_count(frame):
    """All the buttons and labels for the count_frame"""
    # labels
    main.label(frame, "Select product", 20, 40, 50, BG_COLOR)
    main.label(frame, "Number of product", 20, 300, 50, BG_COLOR)

    # entries
    num_entry = tk.Entry(frame, font=('Arial', 15, "bold"), bg=BUTTONS)
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
    Save_changes = tk.Button(frame, text="Save changes", cursor="hand2",
                             font=('Arial', 17, "bold"), bg=BUTTONS, width=19,
                             height=3, highlightcolor=BLACK, bd=1,
                             relief="solid", command=lambda event=None:
                             main.validate(event, num_entry, combo, options,
                                           1))
    Save_changes.place(x=590, y=25)
