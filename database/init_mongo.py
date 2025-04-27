from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin123@mongo:27017/")

if __name__ == "__main__":

    db = client['task_manager']

    users_collection = db['users']
    users_collection.insert_one({
        "username": "ADMIN",
        "password": "$2b$12$UtLUfVqAWwwFa7GGxfoWVOfkdWWgZ0tSh74iRz03niDluo3ZuxOXC",
    })

    print("✅")
