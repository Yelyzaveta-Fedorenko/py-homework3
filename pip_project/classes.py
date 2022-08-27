from exceptions import*
from pyparsing import ParseResults
import pickle
from datetime import datetime
from collections import UserDict


# определяем базовую логику геттеров и сеттеров, которую потом можем переопределять в классах-наследниках
class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)

    # переопределяем сеттер родительского класса на случай, если пользователь не указал имя
    @Field.value.setter
    def value(self, new_value):
        if not new_value:
            raise NoneNameException

        # вызывем метод родительского класса через свойство fset аттрибута property
        Field.value.fset(self, new_value.strip())


class Phone(Field):
    def __init__(self, phone: str):
        super().__init__(phone)

    # переопределяем сеттер родительского класса
    @Field.value.setter
    def value(self, new_value):
        Field.value.fset(self, new_value)

    def __repr__(self):
        return self.value if self.value else 'None'

    def __str__(self):
        return self.__repr__()


class Email(Field):
    def __init__(self, email: str):
        super().__init__(email)

    # переопределяем сеттер родительского класса
    @Field.value.setter
    def value(self, new_value):
        Field.value.fset(self, new_value)

    def __repr__(self):
        return self.value if self.value else 'None'

    def __str__(self):
        return self.__repr__()


class Address(Field):
    def __init__(self, address: ParseResults):
        super().__init__(address)

    # переопределяем сеттер родительского класса
    @Field.value.setter
    def value(self, new_value):
        Field.value.fset(self, new_value)

    def __repr__(self):
        if self.value:
            representation_string = str()
            for key, val in self.value.asDict().items():
                representation_string += f'{key}: {val}\n' if list(
                    self.value.asDict().keys())[-1] != key else f'{key}: {val}'
            return representation_string
        else:
            return 'None'

    def __str__(self):
        return self.__repr__()


class Birthday(Field):
    def __init__(self, date: list):
        super().__init__(date)

    # переопределяем сеттер родительского класса
    @Field.value.setter
    def value(self, new_value):
        new_value = datetime(*new_value).date() if new_value else None
        # вызывем метод родительского класса через свойство fset аттрибута property
        Field.value.fset(self, new_value)

    def __repr__(self):
        return self.value.strftime('%d %B %Y') if self.value else 'None'

    def __str__(self):
        return self.__repr__()


class Record:
    def __init__(self, name: Name, birthday=None, address=None):
        self.name = name
        self.birthday = birthday
        self.address = address
        self.phone_list = []
        self.emails_list = []

    # check if the given phone number already exists
    def add_phone(self, phone: Phone):
        if phone.value not in list(map(lambda phone: phone.value, self.phone_list)):
            self.phone_list.append(phone)
        else:
            raise PhoneAlreadyExistsException

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        phone_matched = list(
            filter(lambda phone: phone.value == old_phone.value, self.phone_list))
        if phone_matched:
            index = self.phone_list.index(*phone_matched)
            self.phone_list[index].value = new_phone.value
        else:
            raise NoSuchPhoneException

    def delete_phone(self, phone: Phone):
        phone_matched = list(
            filter(lambda x: x.value == phone.value, self.phone_list))
        if phone_matched:
            self.phone_list.remove(*phone_matched)
        else:
            raise NoSuchPhoneException

    # check if the given email already exists
    def add_email(self, email: Email):
        if email.value not in list(map(lambda email: email.value, self.emails_list)):
            self.emails_list.append(email)
        else:
            raise EmailAlreadyExistsException

    def change_email(self, old_email: Email, new_email: Email):
        email_matched = list(
            filter(lambda email: email.value == old_email.value, self.emails_list))
        if email_matched:
            index = self.emails_list.index(*email_matched)
            self.emails_list[index].value = new_email.value
        else:
            raise NoSuchEmailException

    def delete_email(self, email: Email):
        email_matched = list(
            filter(lambda x: x.value == email.value, self.emails_list))
        if email_matched:
            self.emails_list.remove(*email_matched)
        else:
            raise NoSuchEmailException

    def change_address(self, new_address: ParseResults):
        self.address = new_address

    def change_birthday(self, new_birthday: Birthday):
        self.birthday = new_birthday

    def days_to_birthday(self):
        now = datetime.now().date()
        nearest_bd = datetime(
            year=now.year, month=self.birthday.value.month, day=self.birthday.value.day).date()
        delta = nearest_bd - now

        if delta.days < 0:
            nearest_bd = nearest_bd.replace(year=nearest_bd.year+1)
            new_delta = nearest_bd - now
            return new_delta.days
        else:
            return delta.days

    def __repr__(self):
        return (f'Name: {self.name.value}\n' +
                f'Phones: {[phone.value for phone in self.phone_list]}\n' +
                f'Emails: {[email.value for email in self.emails_list]}\n' +
                f'Address: \n{self.address}\n' +
                f'Birthday: {self.birthday}\n\n')

    def __str__(self):
        return self.__repr__()


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.iter_index = 0

    # если запись с таким именем уже существует, не добавляем ее
    def add_record(self, record: Record):
        key = record.name.value
        if key not in self.data:
            self.data[key] = record
        else:
            raise RecordAlreadyExistsError

    def get_record(self, name: Name):
        return self.data[name.value]

    def delete_record(self, name: Name):
        del self.data[name.value]

    # поиск записей на основании совпадений введенной строки с любыми из значений полей объекта записи,
    # case insensitive
    def search_records(self, string: str):
        list_of_records = []

        for record in self.data.values():
            list_of_values = []

            for value in record.__dict__.values():
                if isinstance(value, list):
                    [list_of_values.append(item) for item in value]
                elif value is None:
                    continue
                else:
                    list_of_values.append(value)

            for item in list_of_values:
                if string.lower() in str(item.value).lower():
                    list_of_records.append(record)
                    break

        return list_of_records

    # метод для сериализации
    def save_to_file(self, filepath):
        with open(filepath, 'w+b') as file:
            pickle.dump(self, file)

    # метод для десериализации; при восстановлении объекта создаем его глубокую копию
    def restore_from_file(self, filepath):
        with open(filepath, 'r+b') as file:
            restored = pickle.load(file)
            return restored

    # определяем итератор, который быдет разбивать вывод словаря на несколько частей;
    # итератор можно использовать повторно
    def __next__(self):
        keys = list(self.data.keys())
        if self.iter_index <= len(self.data)-1:
            self.iter_index += 1
            return self.data[keys[self.iter_index-1]]
        else:
            self.iter_index = 0
        raise StopIteration

    def __iter__(self):
        return self

    def iterator(self, n: int):
        list_of_data = []
        for _ in range(n):
            try:
                list_of_data.append(next(self))
            except StopIteration:
                if not list_of_data and len(self.data) > 0:
                    list_of_data.append(next(self))
                    continue
                else:
                    break

        return list_of_data

    def __repr__(self):
        string = f''
        for key, val in self.data.items():
            string += f'Record for name {key}:\n{val}'
        return string

    def __str__(self):
        return self.__repr__()
