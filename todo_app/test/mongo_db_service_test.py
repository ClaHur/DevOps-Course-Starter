import pytest
from unittest.mock import patch
import mongomock
from bson import ObjectId
from todo_app.data.mongo_db_service import MongoDbService
import time

@pytest.fixture
def mongo_service():
    with patch('todo_app.data.mongo_db_service.pymongo.MongoClient', new=mongomock.MongoClient):
        service = MongoDbService()
        yield service
        
def test_get_items(mongo_service):
    # Given
    mock_items = [
        {"_id": ObjectId(), "description": "Test Item 1", "status": "todo", "user_id": "userid"},
        {"_id": ObjectId(), "description": "Test Item 2", "status": "done", "user_id": "userid"},
        {"_id": ObjectId(), "description": "Test Item 2", "status": "done", "user_id": "otheruserid"}
    ]
    mongo_service.database.todo_items.insert_many(mock_items)

    # When
    items = mongo_service.get_items("userid") # should only return items with this user id

    # Then
    assert len(items) == 2
    assert items[0].description == "Test Item 1"
    assert items[0].status == "todo"
    assert items[1].description == "Test Item 2"
    assert items[1].status == "done"

def test_add_item(mongo_service):
    # When
    mongo_service.add_item("New Test Item", "userid")

    # Then
    inserted_item = mongo_service.database.todo_items.find_one({"description": "New Test Item"})
    assert inserted_item["description"] == "New Test Item"
    assert inserted_item["status"] == "todo"

def test_update_status(mongo_service):
    # Given
    test_item = {"_id": ObjectId(), "description": "Update Test Item", "status": "todo"}
    mongo_service.database.todo_items.insert_one(test_item)

    # When
    mongo_service.update_status(test_item["_id"], "done")

    # Then
    updated_item = mongo_service.database.todo_items.find_one({"_id": test_item["_id"]})
    assert updated_item["status"] == "done"

def test_delete_item(mongo_service):
    # Given
    test_item = {"_id": ObjectId(), "description": "Delete Test Item", "status": "done"}
    mongo_service.database.todo_items.insert_one(test_item)

    # When
    mongo_service.delete_item(test_item["_id"])

    # Then
    deleted_item = mongo_service.database.todo_items.find_one({"_id": test_item["_id"]})
    assert deleted_item is None

def test_add_user(mongo_service):
    # When
    mongo_service.add_user_if_new('expectedUserId', "expectedUsername")
    mongo_service.add_user_if_new('expectedUserId', "expectedUsername2")

    # Then
    inserted_user = mongo_service.database.users.find_one({"user_id": "expectedUserId"})
    assert inserted_user["user_id"] == 'expectedUserId'
    assert inserted_user["username"] == "expectedUsername"

    inserted_user_duplicate = mongo_service.database.users.find_one({"username": "expectedUsername2"})
    assert inserted_user_duplicate is None

def test_delete_user(mongo_service):
    # Given
    mongo_service.add_user_if_new('adminUser', 'adminUsername', 'admin')
    mongo_service.add_user_if_new('userToRemove', 'userToRemoveUsername')

    # When
    mongo_service.delete_user('userToRemove', 'adminUser')

    # Then
    removed_user = mongo_service.database.users.find_one({"user_id": "userToRemove"})
    assert removed_user is None

def test_toggle_admin(mongo_service):
    # Given
    mongo_service.add_user_if_new('adminUser', 'adminUsername', 'admin')
    mongo_service.add_user_if_new('userToToggle', 'userToToggleUsername', 'user')

    # When
    mongo_service.toggle_admin('userToToggle', 'adminUser')

    # Then
    toggled_user = mongo_service.database.users.find_one({"user_id": "userToToggle"})
    assert toggled_user["role"] == 'admin'

    mongo_service.toggle_admin('userToToggle', 'adminUser')
    toggled_user = mongo_service.database.users.find_one({"user_id": "userToToggle"})
    assert toggled_user["role"] == 'user'

if __name__ == '__main__':
    pytest.main()
