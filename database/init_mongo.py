from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin123@localhost:27017/")

db = client['task_manager']

users_collection = db['users']
users_collection.insert_one({
    "username": "ADMIN",
    "password": "$2b$12$UtLUfVqAWwwFa7GGxfoWVOfkdWWgZ0tSh74iRz03niDluo3ZuxOXC",
})

print("✅ Baza danych i kolekcje utworzone, użytkownik dodany!")
