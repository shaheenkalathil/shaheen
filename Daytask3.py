contacts = {}

while True:
    print("\n===== CONTACT BOOK =====")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. List All Contacts")
    print("6. Exit")

    choice = input("Enter your choice: ")
    if choice == "1":
        name = input("Enter contact name: ")
        phone = input("Enter phone number: ")

        contacts[name] = phone
        print(f"Contact '{name}' added successfully.")
    elif choice == "2":
        name = input("Enter name to search: ")

        phone = contacts.get(name)

        if phone:
            print(f"{name}'s phone number is {phone}")
        else:
            print(f"Contact '{name}' not found.")
    elif choice == "3":
        name = input("Enter name to update: ")

        if name in contacts:
            new_phone = input("Enter new phone number: ")
            contacts[name] = new_phone

            print(f"Contact '{name}' updated successfully.")
        else:
            print(f"Contact '{name}' not found.")
    elif choice == "4":
        name = input("Enter name to delete: ")

        if name in contacts:
            del contacts[name]
            print(f"Contact '{name}' deleted successfully.")
        else:
            print(f"Contact '{name}' not found.")
    elif choice == "5":

        if contacts:
            print("\n--- All Contacts ---")

            for name in sorted(contacts):
                print(f"{name} : {contacts[name]}")
        else:
            print("No contacts available.")
    elif choice == "6" or choice.lower() == "exit":
        print("Exiting Contact Book...")
        break
    else:
        print("Invalid choice. Please try again.")