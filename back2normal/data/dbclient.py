import sqlite3

DB_PATH = "back2normal_db"
PRAGMA_INFO_FIELD_INDEX = 1
PRAGMA_INFO_DTYPE_INDEX = 2


class DBClient:

    def __init__(self, db_path=DB_PATH):

        self.conn = sqlite3.connect(db_path)
        # is it ok to persist this?
        self.cursor = self.conn.cursor()

    def create_table_from_pandas(self, data_df, table_name, replace=True):

        data_df.to_sql(table_name, self.conn, if_exists='replace' if replace else 'fail')

    def get_table_info(self, table_name):

        pragma_statement = f"pragma table_info({table_name})"
        return [(x[PRAGMA_INFO_FIELD_INDEX], x[PRAGMA_INFO_DTYPE_INDEX])
                for x in self.cursor.execute(pragma_statement).fetchall()]
