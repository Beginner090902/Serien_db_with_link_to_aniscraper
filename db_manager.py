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
        #self.conn.execute("PRAGMA foreign_keys = ON")  # FK-Support falls gewünscht

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

    def create_table_alle_namen(self):
        sql = """
        CREATE TABLE IF NOT EXISTS alle_namen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            such_url TEXT NOT NULL
        )
        """
        self.execute(sql)

    def create_table_gefundene_namen(self):
        sql = """
        CREATE TABLE IF NOT EXISTS gefundene_namen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            such_url TEXT NOT NULL,
            seiten_title TEXT,
            year INTEGER
        )
        """
        self.execute(sql)


    def add_name_in_gefundene_namen(self, such_url: str, seiten_title: str, year: int):
        """Datensatz einfügen."""
        sql = f"""
        INSERT INTO gefundene_namen (such_url, seiten_title, year)
        VALUES (?, ?, ?)
        """
        self.execute(sql,(such_url, seiten_title, year))

    def add_name_in_alle_namen(self, such_url):
        sql = f"""
        INSERT INTO alle_namen (such_url)
        VALUES (?)
        """
        self.execute(sql,(such_url,))

    def get_all(self,in_table:str) -> List[Tuple]:
        """Alle Einträge auslesen."""
        sql = f"SELECT * FROM {in_table}"
        cur = self.execute(sql)
        return cur.fetchall()

    def find_by_title(self, such_url: str,in_table) -> List[Tuple]:
        """Sätze zu einem bestimmten Title finden."""
        sql = f"SELECT * FROM {in_table} WHERE such_url LIKE ?"
        cur = self.execute(sql, (f"%{such_url}%",))
        return cur.fetchall()
    
    def delete_all_in_table(self,in_table):
        sql = f"DELETE FROM {in_table}"
        self.execute(sql, params=())
        sql = f"UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='{in_table}'"
        self.execute(sql, params=())

        