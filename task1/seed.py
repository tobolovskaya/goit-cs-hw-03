"""Populate the database with randomly generated data using Faker."""

import psycopg2
from contextlib import contextmanager
from colorama import init, Fore
import faker
from random import randint
from config import DB_CONFIG, NUMBER_USERS, NUMBER_TASKS, STATUSES

# initialise colour output
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


def generate_fake_data(number_users: int, number_tasks: int):
    """Generate fake users and tasks data."""
    fake = faker.Faker()
    fake_users = [
        {"fullname": fake.name(), "email": fake.email()} for _ in range(number_users)
    ]
    fake_tasks = [
        {
            "title": fake.sentence(),
            "description": fake.text(),
            "status_id": randint(1, len(STATUSES)),
            "user_id": randint(1, number_users),
        }
        for _ in range(number_tasks)
    ]

    return fake_users, fake_tasks


def prepare_data(users, statuses, tasks):
    """Prepare generated data for insertion."""
    for_users = [(user["fullname"], user["email"]) for user in users]
    for_statuses = [(status,) for status in statuses]
    for_tasks = [
        (task["title"], task["description"], task["status_id"], task["user_id"])
        for task in tasks
    ]
    return for_users, for_statuses, for_tasks


def insert_data_to_db(users, statuses, tasks) -> None:
    """Insert prepared data into the database tables."""
    with create_connection() as conn:
        try:
            cur = conn.cursor()

            sql_users = """
            INSERT INTO users (fullname, email) VALUES (%s, %s)
            ON CONFLICT (email) DO NOTHING;
            """
            cur.executemany(sql_users, users)
            print(f"{Fore.GREEN}Користувачі успішно додані.")

            sql_status = """
            INSERT INTO status (name) VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
            """
            cur.executemany(sql_status, statuses)
            print(f"{Fore.GREEN}Статуси успішно додані.")

            sql_tasks = """
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (%s, %s, %s, %s);
            """
            cur.executemany(sql_tasks, tasks)
            print(f"{Fore.GREEN}Завдання успішно додані.")

        except Exception as e:  # pragma: no cover - console output only
            print(f"{Fore.RED}Помилка вставки даних: {e}")


if __name__ == "__main__":
    print(f"{Fore.BLUE}Генерація даних...")
    users, tasks = generate_fake_data(NUMBER_USERS, NUMBER_TASKS)
    users, statuses, tasks = prepare_data(users, STATUSES, tasks)

    print(f"{Fore.BLUE}Заповнення бази даних...")
    insert_data_to_db(users, statuses, tasks)
    print(f"{Fore.MAGENTA}База даних успішно заповнена!")
    