# -*- coding:utf-8 -*-

import pymysql
import json
import abc
from jsondiff import diff


class MySQLDDLWatcher(object):
    SCHEME_FILE_FORMAT = "intermediate/{database}.ddlstate"
    IGNORE_TABLES = [
        "mysql",
        "information_schema",
        "performance_schema",
        "sys",
    ]

    def __init__(self, host, port, database, user, password, charset='utf8mb4'):
        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._password = password
        self._charset = charset

        self._connect()

    def _connect(self):
        self._conn = pymysql.connect(host=self._host,
                                     user=self._user,
                                     password=self._password,
                                     db=self._database,
                                     port=self._port,
                                     charset=self._charset,
                                     cursorclass=pymysql.cursors.SSDictCursor)

    def _query(self, query):
        cursor = self._conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        return rows

    def _get_databases(self):
        return self._query("SHOW DATABASES;")

    def _dump_table(self, table_name):
        ret = dict()

        table_descriptions = self._query("DESC {table_name};".format(table_name=table_name))
        for table_description in table_descriptions:
            field = table_description["Field"]
            table_description.pop("Field")
            ret[field] = table_description

        return ret

    def _dump_database(self, database_name):
        self._query("USE {database};".format(database=database_name))
        tables = self._query("SHOW TABLES;")
        table_infos = dict()
        for table in tables:
            table_name = table['Tables_in_{database}'.format(database=database_name)]
            description = self._dump_table(table_name)
            table_infos[table_name] = description

        return table_infos

    def _get_previous_state(self, database_name):
        try:
            filename = self.SCHEME_FILE_FORMAT.format(database=database_name)
            with open(filename, "r") as f:
                prev_database_state = json.loads(f.read())
        except (FileNotFoundError, ValueError) as _:
            prev_database_state = None

        return prev_database_state

    def _diff_scheme(self, database_infos):
        for database_name, info in database_infos.items():
            previous_state = self._get_previous_state(database_name)

            diffs = diff(previous_state, info, syntax='symmetric', dump=True)  # dump for make $ symbol to string key
            diffs = json.loads(diffs)
            if diffs:
                self._notification(diffs)

    def _make_checkpoint(self, database_infos):
        for database_name, info in database_infos.items():
            filename = self.SCHEME_FILE_FORMAT.format(database=database_name)
            with open(filename, "w") as f:
                f.write(json.dumps(info))

    @abc.abstractmethod
    def _notification(self, diffs):
        print(json.dumps(diffs, indent=2))

    def watch(self):
        database_infos = dict()
        databases = self._get_databases()
        for database in databases:
            database_name = database['Database']
            if database_name in self.IGNORE_TABLES:
                continue

            database_info = self._dump_database(database_name)
            database_infos[database_name] = database_info

        self._diff_scheme(database_infos)
        self._make_checkpoint(database_infos)
