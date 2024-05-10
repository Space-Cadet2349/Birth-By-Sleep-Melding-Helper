import tkinter as tk
from tkinter import ttk
import os
import sqlite3

found_rows = []

from tkinter import*



script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, "results.db")


# Create the main window
root = tk.Tk()
root.title("Birth By Sleep: Melding Helper")


#img = PhotoImage(file=str(script_dir) + '\icon.ico')
#tk.Tk().iconphoto(False, img)

# Create a frame for the buttons and dropdown
button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, padx=(0, 0), pady=5, sticky="nw")

# Create BooleanVar variables for button states
aqua_var = tk.BooleanVar()
terra_var = tk.BooleanVar()
ventus_var = tk.BooleanVar()

# Create a label for the first dropdown
letter_label = tk.Label(button_frame, text="Wanted Ability:")
letter_label.grid(row=0, column=1, padx=(5, 120), pady=5, sticky="w")

# Define the options for the first dropdown
options_for_first_dropdown = [
    "","Fire Boost", "Fire Screen", "Blizzard Boost", "Blizzard Screen",
    "Thunder Boost", "Thunder Screen", "Cure Boost", "Dark Screen",
    "Magic Haste", "Reload Boost", "Attack Haste", "Leaf Bracer",
    "Finish Boost", "Second Chance", "Combo F Boost", "Air Combo Plus",
    "Once More", "Combo Plus", "HP Boost", "Damage Syphon",
    "Item Boost", "Defender", "HP Prize Plus", "Treasure Magnet",
    "Link Prize Plus", "EXP Chance", "Lucky Strike", "Luck Boost", "EXP Walker"
]

# Create the first dropdown menu
letter_var = tk.StringVar()
letter_var.set("")  # Set an initial value
letter_dropdown = ttk.Combobox(button_frame, textvariable=letter_var, values=options_for_first_dropdown, width=15)
letter_dropdown.grid(row=0, column=1, padx=(0, 0), pady=5, sticky="e")

# Create a frame for the table
table_frame = ttk.Frame(root)
table_frame.grid(row=0, column=1, padx=0, pady=5, sticky="nwse")

# Create a Treeview widget for a spreadsheet-like table with center-aligned text
table = ttk.Treeview(table_frame, columns=("RecipeName", "FirstIngredient", "SecondIngredient", "Type", "SuccessChance"), show="headings")
table.heading("RecipeName", text="Result")
table.heading("FirstIngredient", text="Slot 1")
table.heading("SecondIngredient", text="Slot 2")
table.heading("Type", text="Item")
table.heading("SuccessChance", text="% Failure Rate")


# Set variable column widths (you can adjust these values)
table.column("RecipeName", width=100)
table.column("FirstIngredient", width=100)
table.column("SecondIngredient", width=100)
table.column("Type", width=60)
table.column("SuccessChance", width=60)

# Create a vertical scrollbar for the table
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=vsb.set)

# Create three toggle buttons with initial state "Off" in the button frame
button1 = tk.Checkbutton(button_frame, text="Aqua Equippable", anchor="e", variable=aqua_var)
button2 = tk.Checkbutton(button_frame, text="Terra Equippable", anchor="e", variable=terra_var)
button3 = tk.Checkbutton(button_frame, text="Ventus Equippable", anchor="e", variable=ventus_var)

# Pack the Table widget and scrollbar to display them in the table frame
table.pack(side="left", fill="both", expand=True)
vsb.pack(side="right", fill="y")

# Configure row and column weights for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the GUI event loop
aqua_pressed = aqua_var.get()
terra_pressed = terra_var.get()
ventus_pressed = ventus_var.get()


def aqua_button_action():
    global aqua_pressed
    aqua_pressed = aqua_var.get()
    print("Aqua button was pressed!")
    fetch_data("")

def terra_button_action():
    global terra_pressed
    terra_pressed = terra_var.get()
    print("Terra button was pressed!")
    fetch_data("")

def ventus_button_action():
    global ventus_pressed
    ventus_pressed = ventus_var.get()
    print("Ventus button was pressed!")
    fetch_data("")

button1 = tk.Checkbutton(button_frame, text="Aqua Equippable", anchor="e", variable=aqua_var, command=aqua_button_action)
button2 = tk.Checkbutton(button_frame, text="Terra Equippable", anchor="e", variable=terra_var, command=terra_button_action)
button3 = tk.Checkbutton(button_frame, text="Ventus Equippable", anchor="e", variable=ventus_var, command=ventus_button_action)


# Pack the buttons to display them in the frame
button1.grid(row=1, column=1, sticky="w")
button2.grid(row=2, column=1, sticky="w")
button3.grid(row=3, column=1, sticky="w")


def fetch_data(ExtraParams):

    global aqua_var, terra_var, ventus_var
    aqua_pressed = aqua_var.get()
    # Construct the path to the database file
    db_path = os.path.join(script_dir, "results.db")

    # Establish a connection to the database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Query to select all data from the "results" table
    print("Ogagagagagagagagagagag" + str(len(found_rows)))
    if (len(found_rows) == 0):   
        query = "SELECT RecipeName, FirstIngredient, SecondIngredient, Type, SuccessChance FROM results"

        # Check the state of the Aqua, Terra, and Ventus buttons
        aqua_pressed = aqua_var.get()
        terra_pressed = terra_var.get()
        ventus_pressed = ventus_var.get()

        # Create a list to hold filtering conditions
        conditions = []

        # Add conditions for the buttons that are pressed
        if aqua_pressed:
            conditions.append('Aqua = "True"')
        if terra_pressed:
            conditions.append('Terra = "True"')
        if ventus_pressed:
            conditions.append('Ventus = "True"')
        if ExtraParams != "":
            conditions.append(ExtraParams)

        # If there are conditions, add a WHERE clause to the query
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            

    print (query)
    # Fetch data from the SQL query
    cursor.execute(query)
    data = cursor.fetchall()

    # Clear existing data in the table
    for item in table.get_children():
        table.delete(item)

    # Insert fetched data into the table
    RowCount = 0
    for row in data:
        recipe_name, slot1, slot2, item_type, success_chance = row

        # Calculate failure rate based on success percentage
        failure_rate = 100 - success_chance

        # Display the failure rate in the "Fail" column
        table.insert("", "end", values=(recipe_name, slot1, slot2, item_type, f"{failure_rate:.2f}%"))
        RowCount = RowCount + 1
    print(RowCount)
    # Close the database connection
    connection.close()

def dropdown_changed(event):
    selected_value = letter_var.get().lower().strip()  # Get the selected value in lowercase and stripped


    script_dir = os.path.dirname(__file__)
    db_path = os.path.join(script_dir, "results.db")


    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Construct a SQL query to select all rows from the table
    query = f"SELECT * FROM CrystalMeldingOutcomes"

    # Execute the query
    cursor.execute(query)
    # Fetch all rows from the table
    all_rows = cursor.fetchall()
    print(all_rows)
    found_rows = []  # To store rows where a match was found

    # Iterate through each row and its index
    for index, row in enumerate(all_rows, start=1):
        # Iterate through each column in the row
        for cell in row:
            if selected_value == str(cell).lower().strip():  # Convert the cell value to lowercase and stripped before comparison
                print(f"Found '{selected_value}' in row {index}")
                found_rows.append(index)  # Store the row index where a match was found


    # Close the database connection
    connection.close()


    # If you found matching rows, you can proceed to filter the results table
    if found_rows:
        filter_results_table(found_rows)
    else:
        # Handle the case where no matching rows were found
        print("No matching rows found.")

def filter_results_table(found_rows):
    global aqua_pressed
    # Construct a SQL query to select rows from the 'results' table where 'type' matches the found row numbers
    query = f"SELECT * FROM results WHERE (type IN ("
    for item in found_rows:
        query = query + str(item) + ","
    query = query[:-1]
    query = query + '))'  

    if (aqua_pressed == True):
        query = query + ' AND ("Aqua" IS "True")'

#    if (terra_var):
 #       query = query + ' AND ("True" IN "Terra")'

#    if(ventus_var):
 #       query = query + ' AND ("True" IN "Ventus")'


    print(query)   
    db_path = os.path.join(script_dir, "results.db")

    # Establish a connection to the database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Execute the query
    cursor.execute(query)

    # Fetch the filtered data
    filtered_data = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Clear existing data in the GUI table
    for item in table.get_children():
        table.delete(item)

    # Insert fetched data into the GUI table
    for row in filtered_data:
        table.insert("", "end", values=row)

    print("Filtered Data:")
    for row in filtered_data:
        print(row)


print("Script Directory:", script_dir)
print("Database Path:", db_path)



# Your code to create the GUI and set up the dropdown and event binding goes here

# Bind the event to the dropdown
letter_dropdown.bind("<<ComboboxSelected>>", dropdown_changed)

letter_dropdown.bind("<<ComboboxSelected>>", dropdown_changed)


root.mainloop()