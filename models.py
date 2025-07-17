from collections import UserDict
from datetime import datetime
import pickle
import os

# Базовий клас для полів
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Клас для зберігання імені
class Name(Field):
    def __init__(self, value):
        if not value or not value.strip():    # Перевірка на порожнє або пробільне ім’я
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

# Клас для зберігання телефону з перевіркою формату
class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:             # перевірка на число і перевірка на 10 цифр
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

# Клас для зберігання дня народження з перевіркою формату
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

# Клас запису контакту        
# клас з методами додавання, редагування, пошуку та видалення номерів
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):                            # Метод __str__ використовується для перетворення об'єкта в рядок під час друку.
        phones = "; ".join(p.value for p in self.phones)    # Цей рядок створює один рядок зі списку номерів, розділений ; (крапка з комою і пробілом).
        bday = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""   # Перевіряю чи день народження існує
        return f"Contact name: {self.name.value}, phones: {phones}{bday}"                           # додаю


# Клас адресної книги
class AddressBook(UserDict):
    def add_record(self, record):                      # record = один контакт (екземпляр (об'єкт) класу Record)
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming = []
        for record in self.data.values():                                 # Проходимося по кожному контакту
            if record.birthday:                                           # Якщо є день народження
                bday = record.birthday.value.replace(year=today.year)     # Отримуємо дату ДН цього року
                if bday < today:
                    bday = bday.replace(year=today.year + 1)              # Якщо вже минув — беремо наступного року
                delta = (bday - today).days                               # Обчислюємо кількість днів до ДН
                if 0 <= delta <= 7:                                       # Якщо менше або дорівнює 7 — додаємо в список
                    upcoming.append(f"{record.name.value}: {bday.strftime('%d.%m.%Y')}")
        return upcoming
    
# Серіалізація та десеріалізація даних

SAVE_FILE = "addressbook.pkl"

# Збереження адресної книги у файл
# Ця функція зберігає об'єкт адресної книги до файлу з допомогою pickle
def save_data(book, filename=SAVE_FILE):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

# Завантаження адресної книги з файлу, або створення нової, якщо файл відсутній
# Ця функція читає файл з адресною книгою, якщо такий існує, або повертає новий об'єкт AddressBook
def load_data(filename=SAVE_FILE):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return AddressBook()