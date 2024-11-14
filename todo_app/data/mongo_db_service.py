import os
import pymongo
from bson import ObjectId
import uuid

from todo_app.models import Item, ListNames, User

class MongoDbService():
    def __init__(self):
        self.database = pymongo.MongoClient(os.getenv('MONGODB_PRIMARY_CONNECTION')).todoapp
        self.list_names = ListNames()
        self.lists_cache = None

    # ITEMS

    def get_items(self, user_id):
        """
        Fetches all items in the mongoDb database for a given user
        """
        todoItems = self.database.todo_items
        items = []
        for item in todoItems.find({"user_id" : user_id}):
            item = Item(item["_id"], item["description"], item["status"])
            items.append(item)

        return items

    def add_item(self, item_name, user_id):
        """
        Adds a new item with the specified title and user id to the mongoDb database
        """
        todoItem = { "description": item_name, "status": "todo", "user_id": user_id }
        self.database.todo_items.insert_one(todoItem)

    def update_status(self, item_id, new_status):
        """
        Updates the status of the item according to the provided status
        """
        todoItems = self.database.todo_items
        todoItems.update_one({"_id": ObjectId(item_id)}, {"$set": {"status": new_status}})

    
    def delete_item(self, item_id):
        """
        Deletes completed items
        """
        todoItems = self.database.todo_items
        todoItems.delete_one({"_id": ObjectId(item_id)})

    # USERS

    def get_users(self):
        """
        Fetches all items in the mongoDb database for a given user
        """
        usersList = self.database.users
        users = []
        for user in usersList.find():
            user = User(user["_id"], user["user_id"], user["role"], user["username"])
            users.append(user)

        return users

    def get_matching_users(self, users, user_id):
        # Ensure user_id is treated as a string, and then apply the regex
        # user_id_str = str(user_id)  # Convert user_id to string if it's not already
        return list(users.find({"user_id": user_id}))
        # return list(users.find({"user_id": {"$regex": f"^{user_id_str}$", "$options": "i"}}))


    def add_user_if_new(self, user_id, username, role = 'user'):
        """
        Adds a new user to the database
        """
        users = self.database.users
        if len(self.get_matching_users(users, user_id)) == 0:
            user = { "user_id": user_id, "username": username, "role": role }
            self.database.users.insert_one(user)
    
    def check_admin_user(self, user_id):
        users = self.database.users
        matching_users = self.get_matching_users(users, user_id)

        if (len(matching_users)) > 0:
            user = matching_users[0]
            if user["role"] == 'admin':
                return True

        return False

    def delete_user(self, user_id, admin_user_id):
        """
        Removes a user and all their associated todo items from the database
        """
        users = self.database.users
        todoItems = self.database.todo_items

        if self.check_admin_user(admin_user_id) == False:
            return False
        
        matching_users = self.get_matching_users(users, user_id)

        if len(matching_users) > 0:
            for user in matching_users: 
                users.delete_one({"_id": ObjectId(user['_id'])})

            for item in todoItems.find({"user_id" : user_id}):
                todoItems.delete_one({"_id": ObjectId(item['_id'])})

            return True
        
        # TODO: Handle the case when the user doesn't exist
        return True
        
    def toggle_admin(self, user_id, admin_user_id):
        """
        Removes a user and all their associated todo items from the database
        """
        if self.check_admin_user(admin_user_id) == False:
            return False
        
        users = self.database.users
        matching_users = self.get_matching_users(users, user_id)

        if len(matching_users) > 0:
            for user in matching_users: 
                new_role = 'user' if user['role'] == 'admin' else 'admin'
                users.update_one({"_id": ObjectId(user['_id'])}, {"$set": {"role": new_role}})

            return True
        
        # TODO: Handle the case when the user doesn't exist
        return True

