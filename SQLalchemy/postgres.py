import sqlalchemy
import os
from sqlalchemy.orm import sessionmaker
from config import *
import models
import atexit


class Postgres:
    def __init__(self):
        if os.path.exists(PASS_PATH):
            with open(PASS_PATH, 'rt') as f:
                password = f.read()
        else:
            if not os.path.exists(PASS_PATH.rpartition('/')[0]):
                os.makedirs(PASS_PATH.rpartition('/')[0])
            password = input(f'Enter password for {USER} to access {DBNAME}: ')
            with open(PASS_PATH, 'wt') as f:
                f.writelines(password)

        self.DSN = f'postgresql://{USER}:{password}@localhost:5432/{DBNAME}'
        self.engine = sqlalchemy.create_engine(self.DSN)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.inspector = sqlalchemy.inspect(self.engine)
        self.models = list(map(lambda class_name: getattr(models, class_name), models.__all__))
        atexit.register(self.terminate)

    def create_tables(self):
        models.Base.metadata.create_all(self.engine)

    def drop_tables(self):
        models.Base.metadata.drop_all(self.engine)

    def check_tables(self):
        result = []
        for model in self.models:
            result.append(self.engine.dialect.has_table(self.engine, model.__tablename__))
        return all(result)

    def get_records(self, table=None):
        """
        The method executes "SELECT *" query for a given table
        or all tables if no arguments given
        table - Can take an str table name or a class from models
        returns: a dict with {table1_name:[(record1)(record2)...],...}
        """
        records = {}
        tables = []
        table_names = self.inspector.get_table_names()

        if table:
            if table not in table_names and table in self.models:
                table = [name for name in table.names if table.__tablename__ == name][0]
            else:
                return 'ERROR: incorrect "table" argument!'
            tables.append(table)
        else:
            tables = table_names

        for table in tables:
            query = f'SELECT * FROM {table}'
            records[table] = self.session.execute(query).fetchall()
        return records

    def select(self, selection, relations=None, filter_=None):
        query = self.session.query(*selection)
        if relations:
            for relation in relations:
                query = query.join(relation)
        if filter_ is not None:
            query = query.filter(filter_)
        return query.all()

    def add_record(self, table_name, **columns):
        model = [m for m in self.models if m.__tablename__ == table_name][0]
        obj = model(**columns)
        self.session.add(obj)
        self.session.commit()

    def terminate(self):
        self.session.close()
        self.engine.dispose()

