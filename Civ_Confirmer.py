import json
import sqlite3
import tkinter as tk
from tkinter import filedialog

global file_path

def Feed_Database():
    database()
    joiner()
    button1.config(command=select_file)
    Label1.config(text="Database was fed")

def select_file():
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    root.deiconify()
    check(file_path)

def check(filepath):

    with open(filepath, 'r') as f:
        data = json.load(f)

    # Connect to the database (creates a new file if it doesn't exist)
    conn = sqlite3.connect('Database/Database.db')
    c = conn.cursor()

    c.execute("SELECT oid, * FROM Final")

    data01 = c.fetchall()

    results = []
    results_stack = 0
    stacking_list = []
    k = 0

    while k < len(data["bonuses"][0]):
        if "and" in data01[data["bonuses"][0][k]][3]:
            stacking_list += [data01[data["bonuses"][0][k]][3].split(" and ")]
        else:
            stacking_list += [data01[data["bonuses"][0][k]][3]]
        k += 1

    for i in data["bonuses"][0]:
        k = 0
        while True:
            if i+1 == data01[k][0]:
                results += [data01[k][2]]
            k += 1
            if k == len(data01):
                break


    results_stack = 0
    if "ARCHER BONUS" in stacking_list and stacking_list.count("ARCHER BONUS") > 0:
        results_stack += (stacking_list.count("ARCHER BONUS"))-1
    if "SIEGE BONUS" in stacking_list and stacking_list.count("SIEGE BONUS") > 0:
        results_stack += (stacking_list.count("SIEGE BONUS"))-1
    if "BUILDING BONUS" in stacking_list and stacking_list.count("BUILDING BONUS") > 0:
        results_stack += (stacking_list.count("BUILDING BONUS"))-1
    if "CAV BONUS" in stacking_list and stacking_list.count("CAV BONUS") > 0:
        results_stack += (stacking_list.count("CAV BONUS"))-1
    if "INFANTRY BONUS" in stacking_list and stacking_list.count("INFANTRY BONUS") > 0:
        results_stack += (stacking_list.count("INFANTRY BONUS"))-1
    if "DISCOUNT BONUS" in stacking_list and stacking_list.count("DISCOUNT BONUS") > 0:
        results_stack += (stacking_list.count("DISCOUNT BONUS"))-1
    if "ECO BONUS" in stacking_list and stacking_list.count("ECO BONUS") > 0:
        results_stack += (stacking_list.count("ECO BONUS"))-1
    if "MISC BONUS" in stacking_list and stacking_list.count("MISC BONUS") > 0:
        results_stack += (stacking_list.count("MISC BONUS"))-1
    if "NAVAL BONUS" in stacking_list and stacking_list.count("NAVAL BONUS") > 0:
        results_stack += (stacking_list.count("NAVAL BONUS"))-1
    if "MONK BONUS" in stacking_list and stacking_list.count("MONK BONUS") > 0:
        results_stack += (stacking_list.count("MONK BONUS"))-1
    if "RESOURCE BONUS" in stacking_list and stacking_list.count("RESOURCE BONUS") > 0:
        results_stack += (stacking_list.count("RESOURCE BONUS"))-1

    # check the bonus type, 3rd place

    text01 = ""
    text02 = ""

    print(results, results_stack)
    print(sum(results) + results_stack)
    if sum(results) + results_stack > 8:
        text01 = "Unaproved with " + str(sum(results) + results_stack - 8) + " points over"
    elif sum(results) + results_stack == 8:
        text01 = "Aproved"
    else:
        text01 = str(8 - (sum(results) + results_stack)) + " points left"

    text02 = str(data["alias"] + "\n\n")
    for i in data["bonuses"][0]:
        text02 += str(data01[i][3] + ", ") + str(data01[i][2]) + ", " + str(data01[i][1] + "\n")

    text02 += "\nStacking Penalty: " + str(results_stack)

    if "UNAVALIBLE" in stacking_list:
        text01 = "This civ has got the one civ bonus which is ilegal, Long Swordsman, Two-Handed Swordsman upgrades available one age earlier"

    lb = [69, 70, 71, 72, 73]
    for i in data["bonuses"][4]:
        if i in lb:
            text01 = "This civ has one of the 5 unavalible Team Bonus"
            break


    Label1.config(text=text01)
    Label2.config(text=text02)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    #Keys: alias, flag_palette, tree, architecture, language, bonuses

def database():
    # Connect to the database (creates a new file if it doesn't exist)
    conn = sqlite3.connect('Database/Database.db')
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS Descriptions")
    c.execute("DROP TABLE IF EXISTS Civ_Bonus")
    c.execute("DROP TABLE IF EXISTS Final")

    # Create a new table
    c.execute("CREATE TABLE IF NOT EXISTS Descriptions (Description TEXT, Points INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS Civ_Bonus (Bonus TEXT, Points REAL, Type TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS Final (Description Text, Points REAL, Type TEXT)")

    # Insert some data

    with open("Database/Lista_CB.txt", "r") as h:
        list00 = [line00.strip() for line00 in h]
    m = 0
    for i in list00:
        c.execute("INSERT INTO Descriptions VALUES (?, ?)", (list00[m], 0))
        m += 1

    c.execute("SELECT * FROM Descriptions")
    teste00 = c.fetchall()


    with open("Database/Lista_bonus.txt", "r") as f:
        list01 = [line01.strip() for line01 in f]

    with open("Database/Lista_pontos.txt", "r") as g:
        list02 = [line02.strip() for line02 in g]

    with open("Database/Lista_types.txt", "r") as u:
        list03 = [line03.strip() for line03 in u]

    n = 0
    for read01 in list01:
        c.execute("INSERT INTO Civ_Bonus (Bonus, Points, Type) VALUES (?, ?, ?)", (list01[n], list02[n], list03[n],))

        n += 1

    c.execute("SELECT * FROM Civ_Bonus")
    teste01 = c.fetchall()

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def joiner():
    # Connect to the database (creates a new file if it doesn't exist)
    conn = sqlite3.connect('Database/Database.db')
    c = conn.cursor()

    # c.execute("DROP TABLE IF EXISTS Final")

    c.execute("SELECT * FROM Civ_Bonus")

    data01 = c.fetchall()

    c.execute("SELECT * FROM Descriptions")

    data02 = c.fetchall()

    l = len(data01)

    data = []
    e = 0
    r = 0
    j = 0

    for i in data02:
        n = 0
        while True:
            if data02[j][0] == data01[n][0]:
                e = 1
                r = n
            n += 1
            if n == l:
                break
        if e == 1:
            data += [(data02[j][0], data01[r][1], data01[r][2])]
        else:
            data += [(data02[j][0], 0, "none")]
        j += 1


    k = 0
    for l in data:
        c.execute("INSERT INTO Final (Description, Points, Type) VALUES (?, ?, ?)", (data[k][0], data[k][1], data[k][2]))
        k += 1

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


file_path = ""
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width // 2
window_height = screen_height // 2
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Get the window's width
window_width = root.winfo_width()

# Calculate 80% of the window's width
label_width = int(window_width * 0.8)

button0 = tk.Button(root, text="Feed database", command=Feed_Database)
button1 = tk.Button(root, text="Check")
Label1 = tk.Label(root)
Label2 = tk.Label(root, anchor="w", justify="left")

button0.place(relheight=0.2, relwidth=0.8, relx=0.1, rely=0.1)
button1.place(relheight=0.2, relwidth=0.8, relx=0.1, rely=0.3)
Label1.place(relheight=0.1, relwidth=0.8, relx=0.1, rely=0.9)
Label2.place(relheight=0.3, relwidth=0.8, relx=0.1, rely=0.5)

root.mainloop()


