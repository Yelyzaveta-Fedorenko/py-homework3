from interface import Interface
from classes import*
from importlib.resources import path


def print_initial_message():
    print('''
        Hello! I"m your virtual assistant. Some words about how I can assist you:
        1) I create a dictionary of records (contacts).
        2) I create a notebook, where you can store, change, delete and search your notes. 
        3) I accept set of commands, that allow to create, change, delete and show records in the address book.
        4) I can sort all files in some given directory.\n
        ''')


def main_book():
    interface = Interface()

    print_initial_message()

    # define exit symbol and exit semaphore
    exit_point = '.'
    exit_flag = False

    while True:
        print('''On this level I accept next commands: hello, good_bye, close, exit, add_record, get_record, search_records, 
                 change_record, show_records, birthday_soon, delete_record\n''')

        # serie of loops to fix the errors on place
        while True:
            input_string = input('''Enter command to create, search, change, show or delete record. 
                                    Or enter one of exit commands to break: \n''')
            first_order_command = interface.parser.handle_first_order_commands(
                input_string)
            first_order_function = interface.first_order_commands_handler(
                first_order_command)

            if first_order_function != None:
                break
        while True:
            func = first_order_function()
            if func == exit_point:
                exit_flag = True
                break
            elif func != None:
                break
        if exit_flag:
            break

    # получаем путь к файлу, в который будем записывать состояние бота на момент завершения его работы
    with path('first_team_project', 'objects_copy.bin') as filepath:
        interface.book.save_to_file(filepath)

    print('Changes saved in objects_copy.bin!\n')
    print('Good bye!\n')


# if __name__ == '__main_book__':
#     main_book()
