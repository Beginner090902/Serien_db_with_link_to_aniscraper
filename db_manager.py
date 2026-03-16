import sqlite3
from typing import List, Tuple, Optional

class DBManager:
    def __init__(self, db_file: str):
        """Erstellt Verbindung zur SQLite-Datenbank."""
        self.db_file = db_file
        self.conn: sqlite3.Connection | None = None
        self._connect()

    def _connect(self):
        """Verbindung öffnen und Cursor erzeugen."""
        self.conn = sqlite3.connect(self.db_file)

    def close(self):
        """Verbindung schließen."""
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def execute(self, sql: str, params: tuple = ()):
        if self.conn is None:
            raise RuntimeError("DB nicht verbunden")

        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur

    # --------------- spezifische Funktionen ----------------

    def create_table(self,table_name: str):

        sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            such_url TEXT NOT NULL,
            real_name TEXT,
            year TEXT,
            image_url TEXT
        )
        """
        self.execute(sql)

    def add_such_url_in_table(self,table_name:str, such_url: str):
        """Datensatz einfügen."""
        sql = f"""
        INSERT INTO {table_name} (such_url)
        VALUES (?)
        """
        self.execute(sql,(such_url,))

    def add_real_name_on_url_in_table(self, real_name:str,such_url:str, table_name:str):
        sql = f"""
        UPDATE {table_name}
        SET real_name = ?
        WHERE such_url = ?
        """
        self.execute(sql,(real_name,such_url))

    def add_year_in_table(self,table_name:str, such_url:str, year:str):
        sql = f"""
        UPDATE {table_name}
        SET year = ?
        WHERE such_url = ?
        """
        self.execute(sql,(year,such_url,))


    def add_image_in_table(self,table_name:str, such_url:str, image_url:str):
        sql = f"""
        UPDATE {table_name}
        SET image_url = ?
        WHERE such_url = ?
        """
        self.execute(sql,(image_url,such_url,))

    def get_all_in_table(self,table_name:str) -> List[Tuple]:
        """Alle Einträge auslesen."""
        sql = f"SELECT * FROM {table_name}"
        cur = self.execute(sql)
        return cur.fetchall()
    
    def get_all_collum_in_table(self,table_name:str,coolum:str) -> List[Tuple]:
        """Alle Einträge auslesen."""
        sql = f"SELECT {coolum} FROM {table_name}"
        cur = self.execute(sql)
        return cur.fetchall()

    def get_serie_information(self,such_url:str,table_name:str):
        sql = f"""
        SELECT * FROM {table_name} WHERE such_url = ?
        """
        cur = self.execute(sql,(such_url,))
        return cur.fetchone()


    def find_by_title_in_table(self, such_url: str,table_name) -> List[Tuple]:
        """Sätze zu einem bestimmten Title finden."""
        sql = f"SELECT * FROM {table_name} WHERE such_url LIKE ?"
        cur = self.execute(sql, (such_url,))
        return cur.fetchall()
    
    def delete_all_in_table(self,table_name):
        sql = f"DELETE FROM {table_name}"
        self.execute(sql, params=())
        sql = f"UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='{table_name}'"
        self.execute(sql, params=())

    def clear_collum(self,table_name:str,collum_name:str):
        sql = f"""
        UPDATE {table_name}
        SET {collum_name} = NULL
        """
        self.execute(sql)
