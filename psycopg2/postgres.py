import psycopg2
import atexit
import os


class Postgres:
    def __init__(self, database, username, password):
        self.connection = psycopg2.connect(database=database,
                                           user=username,
                                           password=password)
        self.cursor = self.connection.cursor()
        atexit.register(self.terminate)
        print(f'<SYSTEM> Postgres: Connected to DB "{database}" as "{username}".')

    def terminate(self):
        """
        The method is called upon exit as per atexit.register
        """
        self.cursor.close()
        self.connection.close()
        print('<SYSTEM> Postgres: Connection to DB terminated. Cursor closed.')

    def execute_script(self, script_path):
        """
        The method to execute a script from file
        returns: True if no exception raised, False otherwise
        """
        success = False
        if not os.path.exists(script_path):
            print(f'<ERROR> File {script_path} not found!')
        else:
            with open(script_path, 'rt', encoding='UTF-8') as filehandle:
                query = filehandle.read()
                success = self.try_commit(query, '<ERROR> Postgres: Could not execute SQL script!')
        return success

    def get_tables(self):
        """
        returns: dict with tables in db.
                {table: {col_number: col_name, ...}, ...}
        """
        query = """\
        SELECT table_name
          FROM information_schema.tables
         WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"""
        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        return tables

    def try_commit(self, query, message='', fetch=False):
        """
        The method receives an SQL query and tries to execute it
        Rolls back changes in case of exception to prevent application drop.
        returns: fetchall result if fetch=True
                 if fetch=False: True if no exception raised, False otherwise
        """
        success = True
        try:
            self.cursor.execute(query)
            if fetch:
                result = self.cursor.fetchall()
            else:
                self.connection.commit()
        except psycopg2.Error as error:
            print(message)
            print(error)
            success = False
            self.connection.rollback()
        return result if fetch and success else success

    def insert_row(self, table, columns, values, returning=''):
        """
        table - table name
        columns - tuple of columns to be filled
        values - tuple of values, len(tuple) and it's order
                 must coincide with columns!
        returns: if not returning:
                 True if no exception raised, False otherwise
                 if returning returns data specified in param
        """
        if len(columns) != len(values):
            print(f'<ERROR> Postgres: Could not insert record!]\n'
                  f'Can not insert {len(values)} '
                  f'values to {len(columns)} columns!')

        fixed_values = tuple()
        for value in values:
            value = str(value)
            value = value.strip("'")
            value = f"'{value}'"
            fixed_values += value,
        values = fixed_values

        query = f"""\
        INSERT INTO {table} ({', '.join(columns)})
        VALUES ({', '.join(values)});"""

        if returning:
            query = query[:-1] + f"\nRETURNING {returning};"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        else:
            success = self.try_commit(query, '<ERROR> Postgres: Could not insert data to table!')
            return success

    def delete_row(self, table, column, target):
        """
        Removes a single row from a specific column.
        table - table name
        column - column name
        target - target str (what should the value in column equal to)
        returns: True if no exception raised, False otherwise
        """
        query = f"""\
        DELETE FROM {table}
         WHERE {column} = '{target}';"""
        success = self.try_commit(query, '<ERROR> Postgres: Could not delete record!')
        return success






