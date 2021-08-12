from tkinter import *
from tkinter import messagebox
from tkinter_constants import *
from db_connect import *

# Establish DB connection
connection = create_connection()
# Create DB Table
execute_query(connection, create_data_table)

root = Tk()

root.config(padx=55, pady=55)
root.eval('tk::PlaceWindow . center')
root.title("Enigma")


# Add/edit person form
def form_window(to_edit=None):
    top = Toplevel(root)
    top.config(padx=30, pady=30)
    top.title("Form")

    # ------------------ Labels ----------------- #
    name_lbl = Label(top, text="Name", font=FONT)
    name_lbl.grid(row=0, column=0, columnspan=2, sticky=W)
    surname_lbl = Label(top, text="Surname", font=FONT)
    surname_lbl.grid(row=2, column=0, columnspan=2, sticky=W)
    email_lbl = Label(top, text="E-mail", font=FONT)
    email_lbl.grid(row=4, column=0, columnspan=2, sticky=W)
    birthday_lbl = Label(top, text="Birthday (dd/mm)", font=FONT)
    birthday_lbl.grid(row=6, column=0, columnspan=2, sticky=W)
    nameday_lbl = Label(top, text="Nameday (dd/mm)", font=FONT)
    nameday_lbl.grid(row=8, column=0, columnspan=2, sticky=W)
    address_lbl = Label(top, text="Address", font=FONT)
    address_lbl.grid(row=10, column=0, columnspan=2, sticky=W)
    interests_lbl = Label(top, text="Interests (csv)", font=FONT)
    interests_lbl.grid(row=12, column=0, columnspan=2, sticky=W)
    phone_lbl = Label(top, text="Phone Number", font=FONT)
    phone_lbl.grid(row=14, column=0, columnspan=2, sticky=W)
    socials_lbl = Label(top, text="Social links", font=FONT)
    socials_lbl.grid(row=16, column=0, columnspan=2, sticky=W)

    # ---------------- Entries ------------------ #
    name_entry = Entry(top, width=FORM_ENTRY_WDTH)
    name_entry.grid(row=1, column=1, padx=FORM_ENTRY_PADX, pady=FORM_ENTRY_PADY)
    surname_entry = Entry(top, width=FORM_ENTRY_WDTH)
    surname_entry.grid(row=3, column=1, padx=FORM_ENTRY_PADX, pady=FORM_ENTRY_PADY)
    email_entry = Entry(top, width=FORM_ENTRY_WDTH)
    email_entry.grid(row=5, column=1, padx=FORM_ENTRY_PADX, pady=FORM_ENTRY_PADY)
    birthday_entry = Entry(top, width=FORM_ENTRY_WDTH)
    birthday_entry.grid(row=7, column=1, padx=FORM_ENTRY_PADX, pady=FORM_ENTRY_PADY)
    nameday_entry = Entry(top, width=FORM_ENTRY_WDTH)
    nameday_entry.grid(row=9, column=1, padx=FORM_ENTRY_PADX, pady=FORM_ENTRY_PADY)
    address_entry = Entry(top, width=FORM_ENTRY_WDTH)
    address_entry.grid(row=11, column=1, padx=FORM_ENTRY_PADX, pady=FORM_ENTRY_PADY)
    interests_entry = Entry(top, width=FORM_ENTRY_WDTH)
    interests_entry.grid(row=13, column=1, padx=FORM_ENTRY_PADX, pady=FORM_ENTRY_PADY)
    phone_entry = Entry(top, width=FORM_ENTRY_WDTH)
    phone_entry.grid(row=15, column=1, padx=FORM_ENTRY_PADX, pady=FORM_ENTRY_PADY)
    socials_entry = Entry(top, width=FORM_ENTRY_WDTH)
    socials_entry.grid(row=17, column=1, padx=FORM_ENTRY_PADX, pady=FORM_ENTRY_PADY)

    # Prepopulate the form if its edit
    if to_edit:
        name_entry.insert(0, to_edit[1])
        surname_entry.insert(0, to_edit[2])
        email_entry.insert(0, to_edit[3])
        birthday_entry.insert(0, to_edit[4])
        nameday_entry.insert(0, to_edit[5])
        address_entry.insert(0, to_edit[6])
        interests_entry.insert(0, to_edit[7])
        phone_entry.insert(0, to_edit[8])
        socials_entry.insert(0, to_edit[9])

    # Clears form entries
    def clear_form():
        email_entry.delete(0, END)
        name_entry.delete(0, END)
        surname_entry.delete(0, END)
        birthday_entry.delete(0, END)
        nameday_entry.delete(0, END)
        address_entry.delete(0, END)
        interests_entry.delete(0, END)
        phone_entry.delete(0, END)
        socials_entry.delete(0, END)

    # Insert Data into DB
    def insert_entry():
        name = name_entry.get()
        surname = surname_entry.get()
        email = email_entry.get()
        birthday = birthday_entry.get()
        nameday = nameday_entry.get()
        address = address_entry.get()
        interests = interests_entry.get()
        phone = phone_entry.get()
        socials = socials_entry.get()

        # Update query
        if to_edit:
            params = (name, surname, email, birthday, nameday, address, interests, phone, socials, to_edit[0])
            if execute_query(connection, update_query, params):
                clear_form()
        # New entry insert query
        else:
            params = (name, surname, email, birthday, nameday, address, interests, phone, socials)
            if execute_query(connection, create_person, params):
                clear_form()

    # ------------------- Buttons ---------------------- #
    add_btn = Button(top, text="Add", width=20, font=FONT, command=insert_entry)
    add_btn.grid(row=18, column=1)

    top.mainloop()


# Search for person window
def search_window():
    top = Toplevel(root)
    top.config(padx=40, pady=25)
    top.title("Search")

    # -------------------- Labels ------------------------- #
    desc = Label(top, text="Search by Name/E-mail", font=FONT)
    desc.grid(row=0, column=0, columnspan=2)
    name_lbl = Label(top, text="Name: ", font=FONT)
    name_lbl.grid(row=1, column=0, pady=5)
    email_lbl = Label(top, text="E-mail: ", font=FONT)
    email_lbl.grid(row=2, column=0, pady=5)

    # ---------- Entries --------- #
    name_entry = Entry(top, width=40)
    name_entry.grid(row=1, column=1, pady=5)
    email_entry = Entry(top, width=40)
    email_entry.grid(row=2, column=1, pady=5)

    # Search Function
    def search_for():
        # try:
        if name_entry.get():
            full_name = name_entry.get().split(" ")
            full_name = [name.title() for name in full_name]
            params = tuple(full_name)
            data = execute_read_query(connection, select_name_query, params)
            if data:
                print(data)
                top.destroy()
                top.update()
                form_window(to_edit=data[0])
            else:
                messagebox.showinfo(title="Oops!", message="No matches found.")
        if email_entry.get():
            email = email_entry.get()
            params = (email,)
            data = execute_read_query(connection, select_email_query, params)
            if data:
                print(data)
                top.destroy()
                top.update()
                form_window(to_edit=data[0])
            else:
                messagebox.showinfo(title="Oops!", message="No matches found.")

    # ------------------------------ Buttons -------------------------------- #
    search = Button(top, text="Search", width=20, command=search_for, font=FONT)
    search.grid(row=3, column=0, columnspan=2, pady=20)

    top.mainloop()


btn1 = Button(root, width=25, text="Add new person", command=form_window)
btn2 = Button(root, width=25, text="Edit/Delete a person", command=search_window)

btn1.grid(row=1, column=0, pady=5)
btn2.grid(row=2, column=0, pady=5)

root.mainloop()
