import psycopg2
import queries as q
from psycopg2 import sql
from create import create_db
from seed import seed_db


def main():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="test_postgres_psw",
        host="localhost",
        port="5432",
    )

    cur = conn.cursor()

    create_db(conn, cur)
    seed_db(conn, cur)

    # 1. Отримати всі завдання певного користувача.
    print(q.get_tasks_by_user(cur, 1))

    # 2. Вибрати завдання за певним статусом.
    print(q.get_tasks_by_status(cur, "in progress"))

    # 3. Оновити статус конкретного завдання.
    print(q.update_task_status(conn, cur, 1, "completed"))

    # 4. Отримати список користувачів, які не мають жодного завдання.
    print(q.get_users_without_tasks(cur))

    # 5. Додати нове завдання для конкретного користувача.
    print(q.add_task(conn, cur, "Add new task", "test test test", 1, 1))

    # 6. Отримати всі завдання, які ще не завершено.
    print(q.get_incomplete_tasks(cur))

    # 7. Видалити конкретне завдання.
    print(q.delete_task(conn, cur, 9))

    # 8. Знайти користувачів з певною електронною поштою.
    print(q.find_users_by_email(cur, "example.net"))

    # 9. Оновити ім'я користувача.
    print(q.update_user_name(conn, cur, 13, "Test user name"))

    # 10. Отримати кількість завдань для кожного статусу.
    print(q.count_tasks_by_status(cur))

    # 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
    print(q.get_tasks_by_email_domain(cur, "example.com"))

    # 12. Отримати список завдань, що не мають опису.
    print(q.get_tasks_without_description(cur))

    # 13. Вибрати користувачів та їхні завдання, які є у статусі.
    print(q.get_users_and_tasks(cur, "in progress"))

    # 14. Отримати користувачів та кількість їхніх завдань.
    print(q.get_users_with_task_counts(cur))

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()