import os
import pymongo
from bson import ObjectId
from flask import session

from todo_app.models import Item, ListNames

class MongoDbService():
    def __init__(self):
        self.database = pymongo.MongoClient(os.getenv('MONGODB_PRIMARY_CONNECTION')).todoapp
        self.list_names = ListNames()
        self.lists_cache = None

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
