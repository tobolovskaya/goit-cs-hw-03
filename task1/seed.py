from faker import Faker
import psycopg2
import random


def seed_db(conn, cur):
    fake = Faker()

    for _ in range(20):
        fullname = fake.name()
        email = fake.email()
        try:
            cur.execute(
                "INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email)
            )
            conn.commit()
        except psycopg2.Error as e:
            print("Error seeding (insert user):", e)
            conn.rollback()

    statuses = ["new", "in progress", "completed"]
    for status in statuses:
        try:
            cur.execute("INSERT INTO status (status_name) VALUES (%s)", (status,))
            conn.commit()
        except psycopg2.Error as e:
            print("Error seeding (insert status):", e)
            conn.rollback()

    for _ in range(20):
        title = fake.sentence()
        description = fake.text()
        status_id = random.randint(1, len(statuses))
        user_id = random.randint(1, 20)
        try:
            cur.execute(
                "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                (title, description, status_id, user_id),
            )
            conn.commit()
        except psycopg2.Error as e:
            print("Error seeding (insert task):", e)
            conn.rollback()