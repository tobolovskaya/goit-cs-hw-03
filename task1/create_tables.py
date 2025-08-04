# Utility for creating the PostgreSQL tables used in the task manager.

import psycopg2
from psycopg2 import Error
from contextlib import contextmanager
from colorama import init, Fore, Style
from config import DB_CONFIG
from colorama import Fore, init

# initialise colorama for coloured terminal output
init(autoreset=True)


@contextmanager
def create_connection():
    """Context manager that yields a PostgreSQL connection."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except Exception as e: # pragma: no cover - console output only
        if conn:
            conn.rollback()
        print(f"{Fore.RED}Помилка підключення: {e}")
    finally:
        if conn:
            conn.close()


def create_table(conn, sql: str) -> None:
    """Execute SQL statement for table creation."""
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        print(f"{Fore.GREEN}Таблиця успішно створена.")
    except Error as e: # pragma: no cover - console output only
        print(f"{Fore.RED}Помилка створення таблиці: {e}")


if __name__ == "__main__":
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE
    );
    """
    sql_create_statuses_table = """
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    );
    """
    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        status_id INTEGER REFERENCES status(id),
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    );
    """

    with create_connection() as conn:
        if conn:
            print(f"{Fore.BLUE}Підключення до бази даних успішне.")

            print(f"{Fore.YELLOW}Створення таблиці 'users'...")
            create_table(conn, sql_create_users_table)

            print(f"{Fore.YELLOW}Створення таблиці 'status'...")
            create_table(conn, sql_create_status_table)

            print(f"{Fore.YELLOW}Створення таблиці 'tasks'...")
            create_table(conn, sql_create_tasks_table)

            print(f"{Fore.MAGENTA}Всі таблиці створені успішно!")
        else:
            print(f"{Fore.RED}Не вдалося створити з'єднання з базою даних.")
            