import sqlite3


class Database:
    DB_NAME = "sms_app.db"

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establish database connection."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.DB_NAME)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def execute(self, query, params=(), commit=True):
        """Execute a query safely."""
        self.connect()
        self.cursor.execute(query, params)
        if commit:
            self.conn.commit()
        return self.cursor

    def executemany(self, query, data):
        """Execute many inserts efficiently."""
        self.connect()
        self.cursor.executemany(query, data)
        self.conn.commit()

    def create_tables(self):
        """Create required tables if they don't exist."""
        self.connect()
        # Contact Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT NOT NULL UNIQUE,
                location TEXT
            );
        """)
        print("Contact Table Created Successfully.")

        # Sent Messages Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sent_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact TEXT NOT NULL,
                message TEXT NOT NULL,
                sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                delivered DATETIME NULL
            );
        """)
        print("Sent Messages Table Created Successfully.")

        self.conn.commit()


if __name__ == "__main__":
    db = Database()
    db.create_tables()
    db.close()