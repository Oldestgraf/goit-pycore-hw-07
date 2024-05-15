from collections import UserDict
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
        pass

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number should has 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            value_date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            print(e)

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            print(e)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(phone)
        print(f"Phone number {phone} isn't found")

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                try:
                    p.value = new_phone
                except ValueError as e:
                    print(e)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        """Celebrating birthdays in next 7 days"""

        date_now = datetime.today().date()
        birthdays = []

        for record in self.data.values:
            user_birthday = record.birthday.value

            # Calculate user birthday in current year
            current_year = date_now.year
            user_birthday_in_current_year = user_birthday.replace(year=current_year)

            # Calculate celebrating including weekends
            congratulation_day = user_birthday_in_current_year.isoweekday()
            if congratulation_day > 5:
                if congratulation_day == 6:
                    birthday = user_birthday_in_current_year + relativedelta(days=2)
                else: birthday = user_birthday_in_current_year + relativedelta(days=1)
            else: birthday = user_birthday_in_current_year

            # Calculate celebrating year
            if birthday < date_now:
                congratulation_date = birthday + relativedelta(years=1)
            else: congratulation_date = birthday

            # Calculate birthdays in the next 7 days
            if date_now < congratulation_date < (date_now + relativedelta(days=7)):
                congratulation_date_str = congratulation_date.strftime("%Y.%m.%d")
                current_user = {"name": record.name.value}
                current_user.update({"congratulation_date": congratulation_date_str})
                birthdays.append(current_user)

        return birthdays

# Створення нової адресної книги
book = AddressBook()

    # Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday("17.05.1976")

    # Додавання запису John до адресної книги
book.add_record(john_record)

    # Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

    # Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

#     # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

#     # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

#     # Видалення запису Jane
# book.delete("Jane")
