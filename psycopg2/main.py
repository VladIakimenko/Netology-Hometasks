from config import *
from queries import *
from postgres import Postgres
from os import path, makedirs
from sys import exit
from json import dump
from string import digits


def cmd_not_found(_dummy):
    print('Command not recognized. Please use one of the following commands:\n'
          ' "execute script" - run SQL script from a file\n'
          ' "add client" - add a new file\n'
          ' "show clients" - show all clients in DB\n'
          ' "find client" - find client by names or contacts\n'
        ''' "change record" - add, change or remove client's details\n'''
          ' "quit" - leave the program'
          )


def execute_script(con):
    print()
    script_path = input(f'Please enter path to SQL Script location: ')
    script_path = script_path.strip().replace('\\', '/')
    if con.execute_script(script_path):
        print()
        print(f'Script {script_path.rpartition("/")[-1]} successfully executed.')


def enter_data(target):
    data = []
    print()
    print('Type "done" to skip/finish entering.')

    while True:
        input_ = input(f'Enter {target}: ')
        input_ = input_.strip('+').strip().replace(' ', '').lower()
        if input_ == 'done':
            break

        if target == 'email' and ('@' not in input_ or '.' not in input_):
            print('Incorrect e-mail!')
            continue

        if target == 'phone number':
            if not input_.isdigit():
                print('Phone can not contain non-digital characters!')
                continue

            input_ = format_phone(input_)
        data.append(input_)
    return data


def format_phone(raw_phone):
    default_country_code = '7'

    raw_phone = raw_phone.replace(' ', '')
    raw_phone = raw_phone.strip('+')

    if raw_phone.startswith('8'):
        raw_phone = raw_phone[1:]
    if len(raw_phone) == 10:
        raw_phone = default_country_code + raw_phone
    result = f'+' \
             f'{raw_phone[:-10]} ' \
             f'{raw_phone[-10:-7]} ' \
             f'{raw_phone[-7:-4]} ' \
             f'{raw_phone[-4:-2]} ' \
             f'{raw_phone[-2:]}'
    return result


def add_client(con):
    client = {'First name': input("Please enter client's First name: ").capitalize().strip(),
              'Last name': input("Please enter client's Last name: ").capitalize().strip(),
              'Phones': enter_data('phone number'),
              'E-mails': enter_data('email')}

    print()
    for key, value in client.items():
        if type(value) == list:
            print()
            print(f'{key}:')
            print(*value, sep='\n')

        else:
            print(f'{key}: {value}')
    print()
    print('Please check the clients details!\n'
          'Save? ("y" or "n"):')
    while True:
        reply = input().lower().strip()
        if reply == 'n':
            return
        elif reply == 'y':
            break

    returning = con.insert_row('clients',
                               ('first_name', 'last_name'),
                               (client['First name'], client['Last name']),
                               returning='client_id')
    client_id = int(returning[0][0])

    phones_query_res = []
    for phone in client['Phones']:
        phones_query_res.append(con.insert_row('phones',
                                               ('phone', 'phone_owner'),
                                               (phone, client_id)))

    emails_query_res = []
    for email in client['E-mails']:
        phones_query_res.append(con.insert_row('emails',
                                               ('email', 'email_owner'),
                                               (email, client_id)))

    if all(phones_query_res) and all(emails_query_res) and client_id:
        print()
        print('Record successfully added.')


def show_clients(con, clients=None):
    if not clients:
        clients = con.try_commit(GET_NAMES, fetch=True)
    for client in clients:
        print(client[1] + ' ' + client[2])
        print('\nPhone numbers:')
        phones = con.try_commit(GET_PHONES.replace('<client_id>', str(client[0])), fetch=True)
        print(*[phone[0] for phone in phones], sep='\n')
        print('\nE-mails:')
        emails = con.try_commit(GET_EMAILS.replace('<client_id>', str(client[0])), fetch=True)
        print(*[email[0] for email in emails], sep='\n')
        print('.' * 60)


def find_client(con):
    search_by = input('Enter search query: ')

    if search_by.strip('+').replace(' ', '').isdigit():
        search_by = format_phone(search_by)

    clients = list(set(con.try_commit(FIND_CLIENT.replace('<value>', search_by), fetch=True)))
    if clients:
        print()
        show_clients(con, clients)
    else:
        print('No records found!')
    return clients


def change_phones_or_emails(con, client, func):
    targets = con.try_commit(func.replace('<client_id>', str(client[0])), fetch=True)
    print()
    print('Choose an option:')
    targets_dict = {}
    for i, target in enumerate(targets, 1):
        print(f'    {i}. Edit {target[0]}')
        targets_dict[i] = target[0]
    else:
        print(f'    0. Add a new {("phone", "e-mail")[func == GET_EMAILS]}')
        print(f'   -1. Delete {("a phone", "an e-mail")[func == GET_EMAILS]}')

    action = ''
    while not action \
            or not all([c in digits + "-" for c in action]) \
            or int(action) not in (range(len(targets) + 1), -1):

        action = input().strip()
        if action == 'abort':
            return

    action = int(action)
    if action != -1:
        input_ = input(f'Enter new {("phone number", "e-mail")[func == GET_EMAILS]}: ')
        if func == GET_PHONES:
            input_ = format_phone(input_)
        else:
            if '@' not in input_ or '.' not in input_:
                print('Incorrect e-mail!')
                return

    if action == 0:
        if con.insert_row(('phones', 'emails')[func == GET_EMAILS],
                          (('phone', 'phone_owner'), ('email', 'email_owner'))[func == GET_EMAILS],
                          (input_, client[0])):
            print('Successfully added!')

    elif action == -1:
        print(f'Choose {("a phone", "an e-mail")[func == GET_EMAILS]} to delete:')
        for i, target in enumerate(targets, 1):
            print(f'    {i}. Edit {target[0]}')

        while True:
            target_choice = input()
            if target_choice \
                    and target_choice.isdigit() \
                    and int(target_choice) in range(1, len(targets) + 1):
                break
            if target_choice == 'abort':
                return

        target_choice = int(target_choice)
        if con.delete_row(('phones', 'emails')[func == GET_EMAILS],
                          ('phone', 'email')[func == GET_EMAILS], targets_dict[target_choice]):
            print('Successfully deleted!')

    else:
        if con.delete_row(('phones', 'emails')[func == GET_EMAILS],
                          ('phone', 'email')[func == GET_EMAILS],
                          targets_dict[action]) and \
            con.insert_row(('phones', 'emails')[func == GET_EMAILS],
                           (('phone', 'phone_owner'), ('email', 'email_owner'))[func == GET_EMAILS],
                           (input_, client[0])):
            print('Successfully substituted!')
    return


def change_names(con, client, _):
    print(f'First name: {client[1]}')
    print(f'Last name: {client[2]}')
    print()
    print('Choose an option:\n'
          '    1. Edit First name\n'
          '    2. Edit Last name\n')

    action = ''
    while not action \
            or not action.isdigit() \
            or int(action) not in range(1, 3):

        action = input().strip()
        if action == 'abort':
            return
        else:
            action = int(action)
            new_name = input(f'Enter new {("First", "Last")[action - 1]} name: ')
            replace = {'<new_value>': new_name,
                       '<table>': 'clients',
                       '<id_column>': 'client_id',
                       '<id>': str(client[0]),
                       '<column>': ('first_name', 'last_name')[action - 1]}
            query = CHANGE_RECORD
            for key, value in replace.items():
                query = query.replace(key, value)

            if con.try_commit(query):
                print('Successfully modified!')


def delete_record(con, client, _):
    phones = con.try_commit(GET_PHONES.replace('<client_id>', str(client[0])), fetch=True)
    emails = con.try_commit(GET_EMAILS.replace('<client_id>', str(client[0])), fetch=True)

    result = []
    for phone in phones:
        result.append(con.delete_row('phones', 'phone', phone[0]))
    for email in emails:
        result.append(con.delete_row('emails', 'email', email[0]))
    result.append(con.delete_row('clients', 'client_id', client[0]))

    if all(result):
        print('Record successfully deleted')


def change_record(con):
    print(f'Please select the record, you want to edit.')
    while True:
        clients = find_client(con)
        if len(clients) == 1:
            break
        elif len(clients) > 1:
            print('There is more that one record selected.\n'
                  'Use another search query to specify the record you want to edit.')
    print()
    print('Please choose what would yo like to edit:\n'
          '    1. Edit names\n'
          '    2. Edit phones\n'
          '    3. Edit e-mails\n'
          '    0. Delete record')

    action = ''
    actions = {1: (change_names, None),
               2: (change_phones_or_emails, GET_PHONES),
               3: (change_phones_or_emails, GET_EMAILS),
               0: (delete_record, None)}

    while not action \
            or not action.isdigit() \
            or int(action) not in range(4):

        action = input().strip()
        if action == 'abort':
            return

    action = int(action)
    actions[action][0](con, clients[0], actions[action][1])


def read_cmd(cmd):
    cmd = cmd.lower().strip()
    if cmd in ('quit', 'q', 'e', 'exit'):
        exit()

    cmd_dict = {'execute script': execute_script,
                'add client': add_client,
                'show clients': show_clients,
                'find client': find_client,
                'change record': change_record,
                '404': cmd_not_found}

    return (cmd_dict['404'], cmd_dict.get(cmd))[cmd in cmd_dict]


def launch():
    print()
    pass_path = PASSWORD_PATH.replace('\\', '/')
    if path.exists(pass_path):
        with open(pass_path, 'rt', encoding='UTF-8') as filehandle:
            password = filehandle.read()
    else:
        password = input(f'Enter password for "{USERNAME}" to access "{DATABASE}" database: ')
        if not path.exists(pass_path.rpartition('/')[0]):
            makedirs(pass_path.rpartition('/')[0])
        with open(pass_path, 'wt', encoding='UTF-8') as filehandle:
            filehandle.writelines(password)

    con = Postgres(DATABASE, USERNAME, password)

    if not path.exists(FLAG):
        if con.execute_script(CREATE_TABLES):
            print(f'Tables have been created and constraints have been set as per {CREATE_TABLES} script.')
            with open(FLAG, 'wt', encoding='UTF-8') as filehandle:
                dump(con.get_tables(), filehandle)
    return con


if __name__ == '__main__':
    connector = launch()

    while True:
        print()
        read_cmd(input('>>> '))(connector)

