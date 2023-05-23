from datetime import datetime
import os


LOG_PATH = 'main.log'


def check_path(path):
    directory = path.replace('\\', '/').rpartition('/')[0]
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def logger_decor(old_function):
    path = LOG_PATH
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)

        dttm = datetime.strftime(datetime.now(), "%H:%M:%S %d.%m.%Y")
        name = old_function.__name__
        arguments = ', '.join([str(arg) for arg in args]) if args else '<no pos. args>'
        kwarguments = (', '.join([f'{key}: {value}' for key, value in kwargs.items()])
                       if kwargs else '<no key-word args>')
        params = f'\t{arguments}\n\t{kwarguments}'
        returned = str(result)

        check_path(path)
        with open(path, 'at', encoding='UTF-8') as filehandle:
            filehandle.write(f'"{name}" function called at {dttm}\n'
                             f'with the following params:'
                             f'\n{params}\n'
                             f'retuning: {returned}\n\n')
        return result
    return new_function


def logger_factory(path):
    def __logger_decor(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)

            dttm = datetime.strftime(datetime.now(), "%H:%M:%S %d.%m.%Y")
            name = old_function.__name__
            arguments = ', '.join([str(arg) for arg in args]) if args else '<no pos. args>'
            kwarguments = (', '.join([f'{key}: {value}' for key, value in kwargs.items()])
                           if kwargs else '<no key-word args>')
            params = f'\t{arguments}\n\t{kwarguments}'
            returned = str(result)

            check_path(path)
            with open(path, 'at', encoding='UTF-8') as filehandle:
                filehandle.write(f'"{name}" function called at {dttm}\n'
                                 f'with the following params:'
                                 f'\n{params}\n'
                                 f'retuning: {returned}\n\n')
            return result
        return new_function
    return __logger_decor
