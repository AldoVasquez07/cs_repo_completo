import configparser
import psycopg2
from psycopg2 import pool

# Leer configuración desde .ini
config = configparser.ConfigParser()
config.read('C:/Users/Aldo/Desktop/Semestre 7/Construccion de Software/repositorio_general/CS_2025_A/proy_blueprints/postgres_config.ini')

dbconfig = {
    "host": config.get("postgresql", "host"),
    "port": config.get("postgresql", "port"),
    "user": config.get("postgresql", "user"),
    "password": config.get("postgresql", "pass"),
    "database": config.get("postgresql", "database")
}

class PostgreSQLPool:
    def __init__(self):
        self.pool = self.create_pool(minconn=1, maxconn=5)

    def create_pool(self, minconn, maxconn):
        return psycopg2.pool.SimpleConnectionPool(
            minconn,
            maxconn,
            **dbconfig
        )

    def close(self, conn, cursor):
        if cursor:
            cursor.close()
        if conn:
            self.pool.putconn(conn)

    def execute(self, sql, args=None, commit=False):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        try:
            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)

            if commit:
                affected_rows = cursor.rowcount
                conn.commit()
                self.close(conn, cursor)
                return affected_rows
            else:
                result = cursor.fetchall()
                self.close(conn, cursor)
                return result
        except Exception as e:
            conn.rollback()
            self.close(conn, cursor)
            raise e


    def executemany(self, sql, args, commit=False):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        try:
            cursor.executemany(sql, args)
            if commit:
                conn.commit()
                self.close(conn, cursor)
                return None
            else:
                result = cursor.fetchall()
                self.close(conn, cursor)
                return result
        except Exception as e:
            conn.rollback()
            self.close(conn, cursor)
            raise e

# Prueba
if __name__ == "__main__":
    pg_pool = PostgreSQLPool()
    sql = "SELECT * FROM autor;"
    results = pg_pool.execute(sql)
    for row in results:
        print(row)
