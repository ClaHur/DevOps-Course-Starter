import pytest
from unittest.mock import patch
import mongomock
from bson import ObjectId
from todo_app.data.mongo_db_service import MongoDbService

@pytest.fixture
def mongo_service():
    with patch('todo_app.data.mongo_db_service.pymongo.MongoClient', new=mongomock.MongoClient):
        service = MongoDbService()
        yield service
        
def test_get_items(mongo_service):
    # Given
    mock_items = [
        {"_id": ObjectId(), "description": "Test Item 1", "status": "todo"},
        {"_id": ObjectId(), "description": "Test Item 2", "status": "done"}
    ]
    mongo_service.database.todo_items.insert_many(mock_items)

    # When
    items = mongo_service.get_items()

    # Then
    assert len(items) == 2
    assert items[0].description == "Test Item 1"
    assert items[0].status == "todo"
    assert items[1].description == "Test Item 2"
    assert items[1].status == "done"

def test_add_item(mongo_service):
    # When
    mongo_service.add_item("New Test Item")

    # Then
    inserted_item = mongo_service.database.todo_items.find_one({"description": "New Test Item"})
    assert inserted_item is not None
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

if __name__ == '__main__':
    pytest.main()
