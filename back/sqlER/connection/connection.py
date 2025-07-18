from typing import Optional
import pyodbc

exclusionTable = ["sys", "INFORMATION_SCHEMA"]


class dbConnection:
    def __init__(
        self,
        driver: Optional[str] = None,
        server: Optional[str] = None,
        database: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        schema: Optional[str] = None,
    ):
        self.driver: Optional[str] = driver
        self.server: Optional[str] = server
        self.database: Optional[str] = database
        self.username: Optional[str] = username
        self.password: Optional[str] = password
        self.schema: Optional[str] = schema

    def __enter__(self):
        self.connection_string: str = f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        self.connection: pyodbc.Connection = pyodbc.connect(self.connection_string)
        self.db_name: str = self.connection.getinfo(pyodbc.SQL_DATABASE_NAME)
        self.db_type: str = self.connection.getinfo(pyodbc.SQL_DBMS_NAME).lower()
        self.schema: str = (
            self.connection.getinfo(pyodbc.SQL_SCHEMA_NAME)
            if self.schema is None
            else self.schema
        )

    def schemas(self):
        sql: str = (
            "SELECT * FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_OWNER = 'dbo';"
        )
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def tables(self, exclusion: bool = True):
        with self.connection.cursor() as cursor:
            results = cursor.tables().fetchall()
        tables = []
        if exclusion:
            global exclusionTable
            for row in results:
                if row[1] not in exclusionTable:
                    tables.append(row)
        else:
            tables = results
        return tables

    def fields(self, table_name: str, schema_name: Optional[str] = None):
        if schema_name is not None:
            full_table_name = f"{schema_name}.{table_name}"
        elif self.schema is not None:
            full_table_name = f"{self.schema}.{table_name}"
        else:
            full_table_name = table_name

        sql: str = f"SELECT * FROM {full_table_name} WHERE 1=0"

        with self.connection.cursor() as cursor:
            cursor.execute(sql)

            return cursor.description

    def selct_all(self, table_name: str, schema_name: Optional[str] = None):
        if schema_name is not None:
            full_table_name = f"{schema_name}.{table_name}"
        elif self.schema is not None:
            full_table_name = f"{self.schema}.{table_name}"
        else:
            full_table_name = table_name

        sql: str = f"SELECT * FROM {full_table_name}"

        with self.connection.cursor() as cursor:
            cursor.execute(sql)

            return {
                "desc": cursor.description,
                "messages": cursor.messages,
                "rowcount": cursor.rowcount,
                "rows": cursor.fetchall(),
            }

    def pk(self, table_name: str, schema_name: Optional[str] = None):
        if schema_name is None:
            schema_name = self.schema
        with self.connection.cursor() as cursor:
            pk_info = cursor.primaryKeys(
                table=table_name, schema=schema_name
            ).fetchall()
            return {
                "desc": cursor.description,
                "messages": cursor.messages,
                "rowcount": cursor.rowcount,
                "primaryKeys": pk_info,
            }

    def fk(self, table_name: str, schema_name: Optional[str] = None):
        if schema_name is None:
            schema_name = self.schema
        with self.connection.cursor() as cursor:
            fk_info = cursor.foreignKeys(
                table=table_name,
                # foreignTable=table_name,
                schema=schema_name,
            ).fetchall()

            return {
                "desc": cursor.description,
                "messages": cursor.messages,
                "rowcount": cursor.rowcount,
                "foreignKeys": fk_info,
            }

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
