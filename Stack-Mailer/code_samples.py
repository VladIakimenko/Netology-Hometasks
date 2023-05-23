SAMPLE_CORRECT = r"""
    def log(old_function):
        def new_function(*args, **kwargs):
            with open(LOG_FILE, 'at', encoding='UTF-8') as filehandle:
                sys.stdout = filehandle
                sys.stderr = filehandle

                name = old_function.__name__
                dttm = datetime.strftime(datetime.now(), "%H:%M:%S %d.%m.%Y")
                arguments = ', '.join([str(arg) for arg in args]) if args else '<no pos. args>'
                kwarguments = (', '.join([f'{key}: {value}' for key, value in kwargs.items()])
                           if kwargs else '<no key-word args>')
                params = f'\t{arguments}\n\t{kwarguments}'

                print(f'"{name}" function called at {dttm}\n'
                      f'with the following params:'
                      f'\n{params}\n')
                try:
                    result = old_function(*args, **kwargs)
                    print(f'{name} function returned:\n{str(result)}\n\n')

                except Exception as e:
                    print(f'Exception raised durning {name} function execution:\n')
                    traceback.print_exc(file=filehandle)
                    print('\n')
                    raise e

            return result
        return new_function
    """
SAMPLE_INCORRECT = r"""
    msg = MIMEMultipart()
    msg['From'] = l
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(message)))

    ms = smtplib.SMTP(GMAIL_SMTP, 587)
    # identify ourselves to smtp gmail client
    ms.ehlo()
    # secure our email with tls encryption
    ms.starttls()
    # re-identify ourselves as an encrypted connection
    ms.ehlo()
    """
