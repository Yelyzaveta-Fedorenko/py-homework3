from address_book_runner import main_book
from Notes import main_notes
from clean import clean_folder


def main():
    answ = ''
    while True:
        answ = input('If U want to work with:\n***' + "\033[0m\033[44m {}" .format('Phone') +
                     '\033[0m' + 'Book ***** ' + "\033[0m\033[44m {}" .format('Note') +
                     '\033[0m' + 's ***** ' + "\033[0m\033[44m {}" .format('Clear') +
                     '\033[0m' + ' Directory *****' '\033[0m' +
                     '\033[44m {}' .format('.') + '\033[0m' + ' - if U want to stop it \n')
        if answ == 'Phone':
            main_book()
        elif answ == 'Note':
            main_notes()
        elif answ == 'Clear':
            clean_folder()
        elif answ == '.':
            print('Good bye!')
            break
        else:
            print('Please, make your choice. And try again.')
            continue


if __name__ == '__main__':
    main()
