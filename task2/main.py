from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from bson.objectid import ObjectId
from faker import Faker

try:
    client = MongoClient(
        "mongodb+srv://************:*********@cluster0.******.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    db = client["cats"]
    collection = db["cats_collection"]
    print("Connected to MongoDB.")
except ConnectionFailure:
    print("MongoDB database connection error.")


# Функція для виведення всіх записів із колекції.
def display_all_cats():
    cats = collection.find()
    if not any(cats):
        print("No cats found.")
    for cat in cats:
        print(cat)


# Функція для виведення інформації про кота за ім'ям
def find_cat_by_name(name):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"No cat with name {name} found.")


# Функція для оновлення віку кота за ім'ям
def update_cat_age(name, new_age):
    try:
        collection.update_one({"name": name}, {"$set": {"age": new_age}})
        print("Cats age was updated.")
    except OperationFailure as e:
        print(f"Error when updating cats name in the database: {e}")


# Функція для додавання нової характеристики до списку features кота за ім'ям
def add_feature_to_cat(name, new_feature):
    try:
        collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        print("New feature was added.")
    except OperationFailure as e:
        print(f"Error when adding new cats feature in the database: {e}")


# Функція для видалення запису з колекції за ім'ям тварини
def delete_cat_by_name(name):
    try:
        collection.delete_one({"name": name})
        print(f"Cat {name} was remodeved.")
    except OperationFailure as e:
        print(f"Error when deleting cat in the database: {e}")


# Функція для видалення всіх записів із колекції
def delete_all_cats():
    try:
        collection.delete_many({})
        print("All cats were removed.")
    except OperationFailure as e:
        print(f"Error when deleting all cats in the database: {e}")


# Функція для створення нового кота
def create_cat(cat):
    try:
        collection.insert_one(cat)
        print(f"Cat {cat.get('name')} was created.")
    except OperationFailure as e:
        print(f"Error when creating new cat in the database: {e}")


# Функція для створення заданої кількості котів
def create_fake_cats(num_cats):
    fake = Faker()
    for _ in range(num_cats):
        cat = {
            "name": fake.first_name(),
            "age": fake.random_int(min=1, max=20),
            "features": [fake.sentence() for _ in range(3)],
        }
        create_cat(cat)
    print(f"Cat were created: {num_cats}.")


if __name__ == "__main__":
    delete_all_cats()
    display_all_cats()
    create_fake_cats(20)
    display_all_cats()
    find_cat_by_name("Scott")

    cat = {
        "name": "Scott",
        "age": 2,
        "features": ["friendly", "cute", "adorable"],
    }

    create_cat(cat)
    find_cat_by_name("Scott")
    update_cat_age("Scott", 4)
    add_feature_to_cat("Scott", "Black & white")
    find_cat_by_name("Scott")
    delete_cat_by_name("Scott")
    find_cat_by_name("Scott")
    display_all_cats()
    delete_all_cats()
    display_all_cats()