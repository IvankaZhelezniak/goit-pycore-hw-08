from models import AddressBook, Record

# Декоратор для обробки помилок введення
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
    return inner

# Обробник команди "add"
@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Please provide both name and phone number.")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

# Обробник команди "change"
@input_error
def change_phone(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Please provide name, old phone, and new phone.")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."
    return "Contact not found."

# Обробник команди "phone"
@input_error    
def get_phones(args, book: AddressBook):
    if not args:
        raise IndexError("Please provide a name.")
    name = args[0]
    record = book.find(name)
    if record:
        return "; ".join(p.value for p in record.phones)
    return "Contact not found."


# Обробник команди "all"
@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."
    contacts = []
    for record in book.data.values():
        contacts.append(str(record))
    return "\n".join(contacts)

# Обробник "add-birthday"
@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Please provide a name and birthday date in DD.MM.YYYY format.")
    name, date_str = args
    record = book.find(name)
    if record:
        record.add_birthday(date_str)
        return "Birthday added."
    return "Contact not found."

# Обробник "show-birthday"
@input_error
def show_birthday(args, book: AddressBook):
    if not args:
        raise IndexError("Please provide a name.")
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    return "Birthday not found."

# Обробник "birthdays"
@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    return "\n".join(upcoming) if upcoming else "No upcoming birthdays."