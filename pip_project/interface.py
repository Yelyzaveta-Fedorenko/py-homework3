from classes import*
from parser import Parser
from decorators import errors_handler
from importlib.resources import path


class Interface:

    # automatically creates the AdressBook object by initialization of Interface object;
    # either create a new object or, if object was already created, restore it from the file
    def __init__(self):
        self.parser = Parser()
        with path('first_team_project', 'objects_copy.bin') as filepath:
            try:
                self.book = AddressBook().restore_from_file(filepath)
                print('Address book was restored from objects_copy.bin')
            except EOFError:
                self.book = AddressBook()

    # commands, that handle exit or continuing of bot-session

    def handle_hello(self):
        print('How can I help you?\n')
        return 0

    def handle_exit(self):
        return '.'

    # auxillary method, that allows to handle possible error while entering the name in while-loop
    @errors_handler
    def create_name(self):
        while True:
            name = input(
                'Please, enter name of contact or print "." to break the loop: \n')
            if name == '.':
                break
            name = Name(name)
            if name != None and name.value in self.book.data.keys():
                break
            elif name != None and name.value not in self.book.data.keys():
                print('There is no such key in address book!')
                continue
        return name

    # auxillary method, that allows to handle possible errors while creating address
    @errors_handler
    def create_address(self):
        def create_default_address():
            print('Address is initialized by default!\n')
            return Address(self.parser.handle_addresses(f'''C:, S:, H:, A:, PC:, End'''))

        city = input(
            'Please, give me city of a contact (optional) or print "." to break the loop \n')
        if city == '.':
            return create_default_address()

        street = input(
            'Please, give me street of a contact (optional) or print "." to break the loop \n')
        if street == '.':
            return create_default_address()

        house_number = input(
            'Please, give me house_number of a contact (optional) or print "." to break the loop \n')
        if house_number == '.':
            return create_default_address()

        flat_number = input(
            'Please, give me flat_number of a contact (optional) or print "." to break the loop \n')
        if flat_number == '.':
            return create_default_address()

        postal_code = input(
            'Please, give me postal_code of a contact (optional) or print "." to break the loop \n')
        if postal_code == '.':
            return create_default_address()

        return Address(self.parser.handle_addresses(f'''C:{city}, S:{street}, H:{house_number}, A:{flat_number}, 
                                                        PC:{postal_code}, End'''))

    # part of methods to handle records (second_order_methods)

    @errors_handler
    def add_phone_number(self):
        name = self.create_name()
        if name == '.':
            return 1
        phone = input(
            'Please, enter phone_number or print "." to break the loop: \n')
        if phone == '.':
            return 1
        phone = Phone(self.parser.handle_phone_numbers(phone))
        self.book.data[name.value].add_phone(phone)
        print('New phone number was added!\n')
        return 0

    @errors_handler
    def add_email(self):
        name = self.create_name()
        if name == '.':
            return 1
        email = input('Please, enter email or print "." to break the loop: \n')
        if email == '.':
            return 1
        email = Email(self.parser.handle_emails(email))
        self.book.data[name.value].add_email(email)
        print('New email was added!\n')
        return 0

    @errors_handler
    def change_phone_number(self):
        name = self.create_name()
        if name == '.':
            return 1

        old_phone = input(
            'Please, enter phone number you want to change, or print "." to break the loop: \n')
        if old_phone == '.':
            return 1

        new_phone = input(
            'Please, enter new phone number or print "." to break the loop: \n')
        if new_phone == '.':
            return 1

        old_phone = Phone(self.parser.handle_phone_numbers(old_phone))
        new_phone = Phone(self.parser.handle_phone_numbers(new_phone))

        self.book.data[name.value].change_phone(old_phone, new_phone)
        print(f'Phone {old_phone.value} was removed with {new_phone.value}!\n')
        return 0

    @errors_handler
    def change_email(self):
        name = self.create_name()
        if name == '.':
            return 1

        old_email = input(
            'Please, enter email you want to change, or print "." to break the loop: \n')
        if old_email == '.':
            return 1

        new_email = input(
            'Please, enter new email or print "." to break the loop:: \n')
        if new_email == '.':
            return 1

        old_email = Email(self.parser.handle_emails(old_email))
        new_email = Email(self.parser.handle_emails(new_email))

        self.book.data[name.value].change_email(old_email, new_email)
        print(f'Email {old_email.value} was removed with {new_email.value}!\n')
        return 0

    @errors_handler
    def change_address(self):
        name = self.create_name()
        if name == '.':
            return 1

        while True:
            address = self.create_address()
            if address != None:
                break
        self.book.data[name.value].change_address(address)
        print('Address was changed!\n')
        return 0

    @errors_handler
    def change_birthday(self):
        name = self.create_name()
        if name == '.':
            return 1

        date = input(
            'Please, enter birthday date or print "." to break the loop: \n')
        if date == '.':
            return 1

        date = Birthday(self.parser.handle_dates(date))
        self.book.data[name.value].change_birthday(date)
        print('Birthday date was changed!\n')
        return 0

    @errors_handler
    def delete_phone(self):
        name = self.create_name()
        if name == '.':
            return 1

        phone = input(
            'Please, enter phone_number you want to delete or print "." to break the loop: \n')
        if phone == '.':
            return 1

        phone = Phone(self.parser.handle_phone_numbers(phone))
        self.book.data[name.value].delete_phone(phone)
        print(f'Phone number {phone.value} was deleted!\n')
        return 0

    @errors_handler
    def delete_email(self):
        name = self.create_name()
        if name == '.':
            return 1

        email = input(
            'Please, enter email you want to delete or print "." to break the loop: \n')
        if email == '.':
            return 1

        email = Email(self.parser.handle_emails(email))
        self.book.data[name.value].delete_email(email)
        print(f'Email {email.value} was deleted!\n')
        return 0

    @errors_handler
    def delete_birthday(self):
        name = self.create_name()
        if name == '.':
            return 1

        self.book.data[name.value].change_birthday(None)
        print('Birthday date was removed!\n')
        return 0

    @errors_handler
    def delete_address(self):
        name = self.create_name()
        if name == '.':
            return 1

        self.book.data[name.value].change_address(None)
        print('Address was removed!\n')
        return 0

    @errors_handler
    def second_order_commands_handler(self, command):
        SECOND_ORDER_COMMANDS = {
            # common_commands
            'hello': self.handle_hello,
            'good_bye': self.handle_exit,
            'close': self.handle_exit,
            'exit': self.handle_exit,

            # commands to handle with Records
            'add_phone': self.add_phone_number,
            'add_email': self.add_email,
            'add_address': self.change_address,
            'add_birthday': self.change_birthday,
            'change_phone': self.change_phone_number,
            'change_email': self.change_email,
            'change_address': self.change_address,
            'change_birthday': self.change_birthday,
            'delete_phone': self.delete_phone,
            'delete_email': self.delete_email,
            'delete_birthday': self.delete_birthday,
            'delete_address': self.delete_address
        }

        return SECOND_ORDER_COMMANDS[command]

    # part of methods to handle address_book (first_order_methods)

    @errors_handler
    def add_record(self):
        name = input('Please, give me name of a contact (necessary): \n')
        if name == '.':
            print('For name was set default value "Name"!')
            name = Name('Name')
        else:
            name = Name(name)

        birthday_date = Birthday(self.parser.handle_dates(
            input('Please, give me birthday date of a contact (optional): \n')))
        if not birthday_date.value:
            print(
                'Birthday date is empty! If you want to change birthday date, use the option "change_birthday!"')

        while True:
            address = self.create_address()
            if address != None:
                break
        record = Record(name, birthday_date, address)
        self.book.add_record(record)
        print('New record was created and added to the address book!\n')
        return 0

    # name loop
    @errors_handler
    def get_record(self):
        name = self.create_name()
        if name == '.':
            return 1

        print(self.book.get_record(name))
        return 0

    def search_record(self):
        string = input(
            'Please, enter the string, you want the records fields to match: \n')
        print(self.book.search_records(string))
        return 0

    @errors_handler
    def show_records(self):
        n_records = int(
            input('Please, specify, how many records are to be shown at once: \n'))
        print(self.book.iterator(n_records))
        return 0

    # @errors_handler
    def records_with_birthday_soon(self):
        n_days = int(
            input('Please, specify the number of days till birthday: \n'))
        contacts = list(filter(lambda x: x.birthday.value and x.days_to_birthday(
        ) <= n_days, self.book.data.values()))
        print(contacts)
        return 0

    # name loop
    @errors_handler
    def delete_record(self):
        name = self.create_name()
        if name == '.':
            return 1
        self.book.delete_record(name)
        print(f'Contact with name {name.value} was deleted!\n')
        return 0

    # essentially this method is interface that allows to handle with second order commands;
    # the logic is familiar with the logic of loop in main()
    def change_record(self):
        # define exit symbol
        exit_point = '.'

        while True:
            print('''On this level I accept next commands: hello, good_bye, close, exit, add_phone, add_email, 
                     add_address, add_birthday, change_phone, change_email, change_address, change_birthday, 
                     delete_phone, delete_email, delete_birthday, delete_address.\n''')

            # define exit semaphore
            exit_flag = False

            # serie of loops to fix the errors on place
            # handle input for second order commands
            while True:
                string = input('''Enter command to change or delete record attributes (phone number, email, birthday date or 
                                  address). Or enter one of exit commands to break: \n''')
                second_order_command = self.parser.handle_second_order_commands(
                    string)
                second_order_function = self.second_order_commands_handler(
                    second_order_command)
                if second_order_function != None:
                    break
            # handle execution of second order command
            while True:
                func = second_order_function()
                if func != None and func == exit_point:
                    exit_flag = True
                    break
                elif func != None and func != exit_point:
                    break
            # if execution is explicit interrupted by entering the exit command, we return to the first commands level
            if exit_flag:
                break
        return 0

    @errors_handler
    def first_order_commands_handler(self, command):
        FIRST_ORDER_COMMANDS = {
            # common_commands
            'hello': self.handle_hello,
            'good_bye': self.handle_exit,
            'close': self.handle_exit,
            'exit': self.handle_exit,

            # commands to handle with AdressBook
            'add_record': self.add_record,
            'get_record': self.get_record,
            'search_records': self.search_record,
            'change_record': self.change_record,
            'show_records': self.show_records,
            'birthday_soon': self.records_with_birthday_soon,
            'delete_record': self.delete_record
        }

        return FIRST_ORDER_COMMANDS[command]
