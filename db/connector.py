from psycopg2.extensions import connection

from app.decorators import ErrorDefender, decorate_all_methods


@decorate_all_methods(ErrorDefender)
class DBConnector(connection):

    sql_functions = ['current_timestamp']

    def __init__(self, db_config):
        super().__init__(dsn=f"host='{db_config.HOST}' "
                             f"port={db_config.PORT} "
                             f"dbname='{db_config.NAME}' "
                             f"user='{db_config.USER}' "
                             f"password='{db_config.PASSWORD}'")

    def insert(self, table_name, data, return_id=False):
        single_row = data if isinstance(data, dict) else data[0]
        sql = f"INSERT INTO {table_name} ({self.generate_columns(single_row)}) VALUES ({self.generate_values(len(single_row.keys()))})"
        if return_id:
            sql += " RETURNING id"
        if isinstance(data, dict):
            with self.cursor() as cursor_obj:
                cursor_obj.execute(sql, self.convert_data(data))
                self.commit()
                if return_id: return cursor_obj.fetchone()[0]
        else:
            with self.cursor() as cursor_obj:
                cursor_obj.executemany(sql, self.convert_data(data))
        self.commit()

    def update(self, table_name, data, where_statements, statement_delimiter='AND', query_extension=None):
        sql = f"UPDATE {table_name} SET {self.generate_statements(data, ',')} WHERE {self.generate_statements(where_statements, statement_delimiter)}"
        if query_extension is not None:
            sql += query_extension
        with self.cursor() as cursor_obj:
            cursor_obj.execute(sql)
            self.commit()

    def delete(self, table_name, where_statements):
        sql = f"DELETE FROM {table_name} WHERE {self.generate_statements(where_statements, 'AND')}"
        with self.cursor() as cursor_obj:
            cursor_obj.execute(sql)
            self.commit()

    def if_exists(self, table_name, where_statements, join_conditions=None, return_dict=None, return_all=False, statement_delimiter='AND', query_extension=None):
        sql = f"SELECT * FROM {table_name}{self.generate_join_statements(join_conditions)} WHERE {self.generate_statements(where_statements, statement_delimiter)}"
        if query_extension is not None:
            sql += query_extension
        with self.cursor() as cursor_obj:
            cursor_obj.execute(sql)
            result = cursor_obj.fetchone() if not return_all else cursor_obj.fetchall()
            return result if return_dict is None else self.get_dict(cursor_obj.description, [result] if not return_all else result)

    def execute_function(self, function_name, params):
        with self.cursor() as cursor_obj:
            cursor_obj.callproc(function_name, params)
            result = cursor_obj.fetchone()
            self.commit()
            if result is None:
                return None
            return result

    def generate_statements(self, statements, statement_delimiter):
        queries = []
        for key, value in statements.items():
            if isinstance(value, str) and value not in self.sql_functions:
                queries.append(f"{key} = '{value}'")
            elif isinstance(value, list):
                queries.append(f"{key} {value[0]} {value[1]}")
            elif value is None:
                queries.append(f'{key} = null')
            else:
                queries.append(f'{key} = {value}')
        return f' {statement_delimiter} '.join(query for query in queries)

    @staticmethod
    def generate_values(num_values):
        return ', '.join('%s' for _ in range(num_values))

    @staticmethod
    def generate_columns(single_row):
        return ', '.join(column for column in single_row.keys())

    @staticmethod
    def generate_join_statements(join_conditions):
        return f' {join_conditions["type"].upper()} JOIN {join_conditions["table"]} ON {join_conditions["condition"]}' \
            if join_conditions is not None else ""

    @staticmethod
    def convert_data(data):
        if isinstance(data, dict):
            return list(data.values())
        else:
            return [list(row.values()) for row in data]

    @staticmethod
    def get_dict(columns, result):
        if (len(result) == 0) or (result[0] is None):
            return {}
        dict_rows = []
        for row in result:
            dict_row = {}
            for column, value in zip(columns, row):
                dict_row[column.name] = value
            dict_rows.append(dict_row)
        return dict_rows
