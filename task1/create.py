import psycopg2
import os


current_file_location = os.path.abspath("create_db.sql")


def create_db(conn, cur):
    if os.path.exists(current_file_location):
        with open(current_file_location, "r") as f:
            sql = f.read()
        try:
            cur.execute(sql)
            conn.commit()
        except psycopg2.Error as e:
            print("Error tables creation:", e)
            conn.rollback()
    else:
        print(f"File {file_path} not found.")