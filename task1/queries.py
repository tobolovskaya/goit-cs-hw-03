"""Helper script containing SQL queries for the task manager."""

from contextlib import contextmanager
import logging

import psycopg2
from psycopg2 import OperationalError
from colorama import init, Fore

from config import DB_CONFIG

init(autoreset=True)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@contextmanager
def create_connection():
    """Yield a database connection."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except OperationalError as e: # pragma: no cover - console output only
        logger.error("Помилка підключення: %s", e)
        if conn:
            conn.rollback()
    except Exception as e:
        logger.error("Невідома помилка: %s", e)
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


def execute_query(sql: str, params: tuple = (), query_number: int = 1) -> None:
    """Execute a given SQL query and print the results."""
    print(f"\n{Fore.BLUE}--- Запит {query_number} ---")
    try:
        with create_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            if sql.strip().upper().startswith("SELECT"):
                for row in cur.fetchall():
                    print(row)
            else:
                print(f"{Fore.GREEN}Запит виконано успішно.")
                logger.info("Запит %s виконано успішно.", query_number)
    except Exception as e:  # pragma: no cover - console output only
        logger.error("Помилка виконання запиту %s: %s", query_number, e)
        print(f"{Fore.RED}Помилка виконання запиту.")


if __name__ == "__main__":
    # 1. Отримати всі завдання певного користувача
    user_id = 2
    sql_1 = """
    SELECT *
    FROM tasks
    WHERE user_id = %s;
    """
    execute_query(sql_1, (user_id,), query_number=1)

    # 2. Вибрати завдання за певним статусом
    status_name = "new"
    sql_2 = """
    SELECT *
    FROM tasks
    WHERE status_id = (SELECT id FROM status WHERE name = %s);
    """
    execute_query(sql_2, (status_name,), query_number=2)

    # 3. Оновити статус конкретного завдання
    task_id = 1
    new_status = "in progress"
    sql_3 = """
    UPDATE tasks
    SET status_id = (SELECT id FROM status WHERE name = %s)
    WHERE id = %s;
    """
    execute_query(sql_3, (new_status, task_id), query_number=3)

    # 4. Отримати список користувачів без завдань
    sql_4 = """
    SELECT *
    FROM users
    WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);
    """
    execute_query(sql_4, query_number=4)

    # 5. Додати нове завдання для конкретного користувача
    sql_5 = """
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s);
    """
    execute_query(
        sql_5,
        ("New Task", "Description of new task", "new", 2),
        query_number=5,
    )

    # 6. Отримати всі завдання, які ще не завершено
    sql_6 = """
    SELECT * FROM tasks
    WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
    """
    execute_query(sql_6, query_number=6)

    # 7. Видалити конкретне завдання
    sql_7 = """
    DELETE FROM tasks WHERE id = %s;
    """
    execute_query(sql_7, (1,), query_number=7)

    # 8.Знайти користувачів з певною електронною поштою
    email_pattern = "%@example.com"
    sql_8 = """
    SELECT * FROM users WHERE email LIKE %s;
    """
    execute_query(sql_8, ("%@example.com",), query_number=8)

    # 9.Оновити ім'я користувача
    sql_9 = """
    UPDATE users SET fullname = %s WHERE id = %s;
    """
    execute_query(sql_9, ("Updated Name", 1), query_number=9)

    # 10.Отримати кількість завдань для кожного статусу
    sql_10 = """
    SELECT s.name, COUNT(t.id) AS task_count
    FROM status s
    LEFT JOIN tasks t ON s.id = t.status_id
    GROUP BY s.name;
    """
    execute_query(sql_10, query_number=10)

    # 11. Отримати завдання, які призначені користувачам з певною доменною частиною
    sql_11 = """
    SELECT t.*
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE %s;
    """
    execute_query(sql_11, ("%@example.com",), query_number=11)

    # 12. Отримати список завдань без опису
    sql_12 = """
    SELECT * FROM tasks WHERE description IS NULL;
    """
    execute_query(sql_12, query_number=12)

    # 13. Вибрати користувачів та їхні завдання у статусі 'in progress'
    sql_13 = """
    SELECT u.fullname, t.title
    FROM users u
    JOIN tasks t ON u.id = t.user_id
    WHERE t.status_id = (SELECT id FROM status WHERE name = %s);
    """
    execute_query(sql_13, ("in progress",), query_number=13)

    # 14.Отримати користувачів та кількість їхніх завдань
    sql_14 = """
    SELECT u.fullname, COUNT(t.id) AS task_count
    FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.fullname;
    """
    execute_query(sql_14, query_number=14)