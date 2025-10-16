import os
import sqlite3

db = sqlite3.connect("Contacts.db")
cr = db.cursor()

Welcome_message = "\n\n" + "#" * 40 + "\n" + " Welcome to the Contacts App! ".center(40, "#") + "\n" + "#" * 40

input_message = """

Please choose an option:
1. Add Contact
2. View Contacts
3. Find Contact by ID
4. Update Contact
5. Delete Contact
6. Exit

Enter your choice (1-6): """

separator = "\n" + "-" * 40 + "\n"


def create_table():
    """Create the contacts table if it doesn't exist."""
    cr.execute("CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT)")
    db.commit()

create_table()

def decorate_header(text):
    """Decorate a header text with '#' characters."""
    return "\n" + "#" * 40 + "\n" + f" {text} ".center(40, "#") + "\n" + "#" * 40

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def go_back_to_main_menu():
    """Pause and wait for user input to go back to the main menu."""
    print("\n\n")

    os.system('pause' if os.name == 'nt' else 'read -n 1 -s -r -p "Press any key to go back to main menu..."')

def is_contact_exists(contact_id):
    """Check if a contact ID exists in the database."""
    cr.execute("SELECT id FROM contacts WHERE id = ?", (contact_id,))
    return cr.fetchone() is not None

def add_contact():
    """Add a new contact to the database."""
    clear_screen()
    print(decorate_header(" Add New Contact Screen "))

    while True:

        id = input("\nEnter Contact ID: ")
        if is_contact_exists(id):
            print("ID already exists. Please try again.")
            continue
        elif not id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            continue
        else:
            break


    name = input("Enter Contact Name: ")
    phone = input("Enter Contact Phone: ")
    email = input("Enter Contact Email: ")

    infos = (int(id), name, phone, email)

    cr.execute("INSERT INTO contacts(id, name, phone, email) VALUES(?, ?, ?, ?)", infos)

    print(f"\nContact with ID {id} has been added.\n")

    db.commit()

    go_back_to_main_menu()

def view_contact(id):
    """View a specific contact by ID."""
    
    while True:
        if not is_contact_exists(id):
            print("Contact not found. Please try again.")
            continue

        cr.execute("SELECT * FROM contacts WHERE id=?", (id,))
        row = cr.fetchone()
        print(f"\nContact Details:\nID: {row[0]}\nName: {row[1]}\nPhone: {row[2]}\nEmail: {row[3]}\n")
        break

def find_contact():
    """Find and display a contact by ID."""
    clear_screen()
    print(decorate_header(" Find Contact Screen "))


    id = int(input("\nEnter the ID of the contact to find: "))
    view_contact(id)

    db.commit()

    go_back_to_main_menu()

def view_all_contacts():
    """View all contacts in the database."""
    clear_screen()
    print(decorate_header(" View All Contacts Screen "))


    cr.execute("SELECT * FROM contacts")
    rows = cr.fetchall()

    print(f"\nYou have {len(rows)} contacts:" if len(rows) > 0 else "\nYou have no contacts to show.")
    
    if len(rows) > 0:
        for counter, row in enumerate(rows):
            print("\n--------------------")
            print(f"Contact #{counter + 1}:\n")
            print(f"ID: {row[0]}\nName: {row[1]}\nPhone: {row[2]}\nEmail: {row[3]}")

    db.commit()

    go_back_to_main_menu()

def update_contact():
    """Update an existing contact in the database."""

    clear_screen()
    print(decorate_header(" Update Contact Screen "))


    while True:
        id = int(input("\nEnter the ID of the contact to update: "))
        if not is_contact_exists(id):
            print("Contact not found. Please try again.")
            continue

        view_contact(id)

        optional_to_update = input(f"\nAre you sure you want to update contact with ID {id}? (y/n): ").lower()
        if optional_to_update != 'y':
            print("Update cancelled.")
            break

        name = input("Enter new Contact Name: ")
        phone = input("Enter new Contact Phone: ")
        email = input("Enter new Contact Email: ")

        infos = (name, phone, email, id)

        cr.execute("UPDATE contacts SET name=?, phone=?, email=? WHERE id=?", infos)
        break

    print(f"\nContact with ID {id} has been updated.\n")
    
    db.commit()

    go_back_to_main_menu()

def delete_contact():
    """Delete a contact from the database."""
    clear_screen()
    print(decorate_header(" Delete Contact Screen "))


    while True:
        id = int(input("\nEnter the ID of the contact to delete: "))
        if not is_contact_exists(id):
            print("Contact not found. Please try again.")
            continue

        view_contact(id)

        option_to_delete = input(f"\nAre you sure you want to delete contact with ID {id}? (y/n): ").lower()
        if option_to_delete != 'y':
            print("Deletion cancelled.")
            break

        cr.execute("DELETE FROM contacts WHERE id=?", (id,))
        print(f"Contact with ID {id} has been deleted.")
        break

    db.commit()

    go_back_to_main_menu()

def commit_and_close():
    """Commit changes and close the database connection."""
    db.commit()
    db.close()
    

while True:
    
    clear_screen()

    print(Welcome_message)

    user_input = input(input_message)

    print(separator)

    if user_input == "1":
        add_contact()

    elif user_input == "2":
        view_all_contacts()

    elif user_input == "3":
        find_contact()

    elif user_input == "4":
        update_contact()

    elif user_input == "5":
        delete_contact()

    elif user_input == "6":
        print("Exiting the Contacts App. Goodbye!")
        commit_and_close()
        break

    else:
        print("\nInvalid choice. Please enter a number between 1 and 6.")
    
    print(separator)


