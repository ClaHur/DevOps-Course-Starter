import os
import pickle
from dotenv import load_dotenv, find_dotenv
import pytest
import requests
from todo_app import app
from todo_app.test.test_data.testing_data import TestData

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data


def stub(url, params={}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')

    url_mappings = {
        f'https://api.trello.com/1/boards/{test_board_id}/lists': TestData.fake_lists,
        f'https://api.trello.com/1/boards/{test_board_id}/cards': TestData.fake_cards,
        f'https://api.trello.com/1/list/{TestData.fake_to_do_list_id}': TestData.fake_to_do_list,
        f'https://api.trello.com/1/list/{TestData.fake_in_progress_list_id}': TestData.fake_in_progress_list,
        f'https://api.trello.com/1/list/{TestData.fake_done_list_id}': TestData.fake_done_list
    }

    fake_response_data = url_mappings.get(url)
    if fake_response_data is not None:
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')

def test_index_page(monkeypatch, client):
    def mock_pickle_load(args):
        raise FileNotFoundError
    def mock_pickle_dump(data, file):
        return
    monkeypatch.setattr("todo_app.data.session_items.pickle.load", mock_pickle_load)
    monkeypatch.setattr("todo_app.data.session_items.pickle.dump", mock_pickle_dump)
    monkeypatch.setattr(requests, 'get', stub)

    response = client.get('/')

    assert response.status_code == 200
    assert 'To Do Card' in response.data.decode()
    assert 'In Progress Card' in response.data.decode()
    assert 'Done Card' in response.data.decode()