import re
from dotenv import load_dotenv, find_dotenv
import pytest
from todo_app import app
import mongomock
from todo_app.assets.constants import in_progress_status
from todo_app.data.mongo_db_service import MongoDbService

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client
            
def test_index_page(client):
    # When
    response = client.get('/')

    # Then
    assert response.status_code == 200
    print(response.data.decode())
    assert "Clare's todo list" in response.data.decode()
    assert 'What do you need to do?' in response.data.decode()
    assert 'Add item' in response.data.decode()

def test_adding_item(client):
    # When
    response = client.post('/add_item', data={
        'todo': 'Test item',
    }, follow_redirects=True)

    # Then
    assert "Clare's todo list" in response.data.decode()
    assert 'Test item' in response.data.decode()


def test_updating_item_status(client):
    # Given
    response = client.post('/add_item', data={
        'todo': 'Test item',
    }, follow_redirects=True)
    itemId = str(MongoDbService().get_items()[0].id)

    # When
    response = client.post('/update_status', 
                        json={'itemId': itemId, 'newStatus': in_progress_status}, 
                        follow_redirects=True)
    
    # Then
    # Verify 'Test item' is in the 'In Progress' column
    pattern = r'(In Progress)(.|\n)*(Test item)(.|\n)*(Done)'
    match = re.search(pattern, response.data.decode())
    assert match is not None

def test_deleting(client):
    # Given
    response = client.post('/add_item', data={
        'todo': 'Test item',
    }, follow_redirects=True)
    itemId = str(MongoDbService().get_items()[0].id)

    # When
    response = client.post('/delete_item', 
                        json={'itemId': itemId}, 
                        follow_redirects=True)
    
    # Then
    assert 'Test item' not in response.data.decode()

