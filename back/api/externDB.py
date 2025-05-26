import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="zjj",
        host="127.0.0.1",
        port=3306,
        database="test",
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


# create a table and a table foreign key create
def create_table():
    try:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100))"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, FOREIGN KEY (user_id) REFERENCES users(id))"
        )
        conn.commit()
    except mariadb.Error as e:
        print(f"Error creating tables: {e}")
        conn.rollback()


# show all tables and their foreign keys and primary keys
def show_tables():
    try:
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        for table in tables:
            print(f"Table: {table[0]}")
            cur.execute(f"SHOW CREATE TABLE {table[0]}")
            create_statement = cur.fetchone()[1]
            print(f"Create Statement: {create_statement}")
    except mariadb.Error as e:
        print(f"Error showing tables: {e}")


if __name__ == "__main__":
    create_table()
    show_tables()
    cur.close()
    conn.close()
