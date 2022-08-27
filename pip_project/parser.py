from pyparsing import*
from decorators import errors_handler
from exceptions import EmailLengthException


class Parser:
    def __init__(self):
        self.first_order_commands = ['hello', 'good_bye', 'close', 'exit', 'add_record', 'get_record', 'search_records',
                                     'change_record', 'show_records', 'birthday_soon', 'delete_record']
        self.second_order_commands = ['hello', 'good_bye', 'close', 'exit', 'add_phone', 'add_email', 'add_address',
                                      'add_birthday', 'change_phone', 'change_email', 'change_address', 'change_birthday',
                                      'delete_phone', 'delete_email', 'delete_address', 'delete_birthday']

    def commands_parser(self, string: str, commands: list):
        # delimiter may be any printable char including space and except alphas
        delimiter = Word(
            printables + ' ', excludeChars=alphas).leaveWhitespace().setParseAction(replaceWith('_'))
        parser = Optional(Word(alphas) + ZeroOrMore(Suppress(delimiter) + Word(alphas))).setParseAction(lambda t:
                                                                                                        [i.lower() for i in t.asList()])

        # replace all possible delimiters with '_' to uniform the string
        parser.transformString(string)

        # parse the string based on the '_' delimiter
        string_items = parser.parseString(string, parseAll=True)

        # create dict in form of {index of matched command : command}, so that we recieve the ordered dict of commands,
        # according to the order, in which commands were given in input string

        dict_of_commands = dict()

        for i in commands:
            if i in '_'.join(string_items) and i not in dict_of_commands:
                dict_of_commands['_'.join(string_items).find(i)] = i
            elif i.replace('_', '') in ''.join(string_items) and i not in dict_of_commands:
                dict_of_commands[''.join(string_items).find(
                    i.replace('_', ''))] = i
            else:
                continue

        # create list of sorted match positions
        sorted_keys = sorted(dict_of_commands.keys())

        if len(dict_of_commands) > 1 and dict_of_commands[sorted_keys[0]] == 'hello':
            return dict_of_commands[sorted_keys[1]]
        elif not dict_of_commands:
            return ''
        else:
            return dict_of_commands[sorted_keys[0]]

    @errors_handler
    def handle_first_order_commands(self, input_string: str):
        return self.commands_parser(input_string, self.first_order_commands)

    @errors_handler
    def handle_second_order_commands(self, input_string: str):
        return self.commands_parser(input_string, self.second_order_commands)

    def handle_phone_numbers(self, phone: str):
        symbols = '()- '
        phone_parser = Combine(Optional(
            Suppress('+')) + ZeroOrMore(Optional(Suppress(Word(symbols))) + Word(nums)))

        return phone_parser.parseString(phone).asList()[0]

    def handle_emails(self, email: str):
        # spaces are not allowed within the local part, only in a form of " "@example.com;
        # one backslash is not allowed, only double;
        # double quotes are not allowed within local part;
        # domain cannot have a form of ip-address

        quoted_chars = '(),:;<>@[]'
        unquoted_chars = "!#$%&'*+-/=?^_`{|}~"

        quote_lit = Literal('"')
        dot_lit = Literal('.')
        space_lit = White()

        unquoted_unit = Word(alphanums + unquoted_chars) + ZeroOrMore(
            Optional(Literal('.')) + Word(alphanums + unquoted_chars))
        quoted_unit = Word(alphanums + unquoted_chars +
                           quoted_chars + '.' + '\\')

        local_part = Combine(ZeroOrMore((quote_lit + quoted_unit + quote_lit + dot_lit) | (unquoted_unit + dot_lit)) +
                             ((quote_lit + quoted_unit + quote_lit) | unquoted_unit | (quote_lit + space_lit + quote_lit)))('local_part')

        domain = Combine(ZeroOrMore(OneOrMore(Word(alphanums) + Optional((Literal('-')) + Word(alphanums))) + dot_lit) +
                         Word(alphanums))('domain')

        email_parser = Optional(
            Combine(local_part + Literal('@') + domain + StringEnd()))

        checked_mail = email_parser.parseString(email)

        if len(checked_mail.local_part) > 64:
            raise EmailLengthException
        else:
            return checked_mail.asList()[0]

    def handle_addresses(self, address: str):
        delim = Word(',;.')

        city = Word(alphas + '- ')('city') + Suppress(delim)
        street = Word(alphanums + "-/'() ")('street') + Suppress(delim)
        house = Word(alphanums + '-_/()')('house') + Suppress(delim)
        appartment = Word(alphanums + '_-/()')('appartment') + Suppress(delim)
        postal_code = Word(nums)('postal_code') + Suppress(delim)

        address_parser = ('C:' + Suppress(Optional(delim)) + Optional(city) +
                          'S:' + Suppress(Optional(delim)) + Optional(street) +
                          'H:' + Suppress(Optional(delim)) + Optional(house) +
                          'A:' + Suppress(Optional(delim)) + Optional(appartment) +
                          'PC:' + Suppress(Optional(delim)) + Optional(postal_code) +
                          'End')

        return address_parser.parseString(address)

    def handle_dates(self, date: str):
        delimiters = '.,/\+-*|:;'
        days_digits = ''.join([str(i) for i in range(1, 32)])
        months_digits = ''.join([str(i) for i in range(1, 13)])

        delimiter_unit = Word(delimiters) | White()
        days_unit = Word(days_digits)
        months_unit = Word(months_digits)

        date_unit = (Optional(Combine(Optional('0') + days_unit) + Suppress(delimiter_unit) +
                              Combine(Optional('0') + months_unit) + Suppress(delimiter_unit) +
                              Combine(Char(nums) * (1, 4))).setParseAction(lambda t: [int(i) for i in t.asList() if i]))

        # form the list in reversed order so that it will be easy to create a datetime object
        list_of_date_units = date_unit.parseString(date).asList()[::-1]

        return list_of_date_units
