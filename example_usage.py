from models import AddressBook, Record

book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
book.add_record(john_record)

# Створення запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Вивід записів
for name, record in book.data.items():
    print(record)

# Редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print(john)

# Пошук телефону
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")

# Видалення Jane
book.delete("Jane")
