from flask import session
import requests
import os

class Item:
    def __init__(self, id, name, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], list['name'])

board_id = os.getenv("TRELLO_BOARD_ID")
api_key = os.getenv("TRELLO_API_KEY")
token = os.getenv("TRELLO_TOKEN")

base_trello_url = "https://api.trello.com/1"

def get_lists():
    """
    Returns all the lists on the trello board
    """
    url = f"{base_trello_url}/boards/{board_id}/lists"
    params = {
        "key" : api_key,
        "token" : token
    }

    response = requests.get(url, params=params)
    response_json = response.json()

    return response_json

def get_list(list_id):
    """
    Returns a list of a given ID
    """
    url = f"{base_trello_url}/list/{list_id}"
    params = {
        "key" : api_key,
        "token" : token
    }

    response = requests.get(url, params=params)
    response_json = response.json()

    return response_json

def get_items():
    """
    Fetches all items on the trello board
    """
    url = f"{base_trello_url}/boards/{board_id}/cards"
    params = {
        "key" : api_key,
        "token" : token
    }

    response = requests.get(url, params=params)
    response_json = response.json()

    items = []
    for card in response_json:
        item = Item.from_trello_card(card, get_list(card["idList"]))
        items.append(item)

    return items

def get_item(id):
    """
    Fetches the item with the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the list.
    """
    list_id = get_lists()[0]["id"]
    url = f"{base_trello_url}/cards"
    params = {
        "idList": list_id,
        "key" : api_key,
        "token" : token,
        "name" : title
    }

    response = requests.post(url, params=params)

    return response

def update_status(item_id, is_checked):
    """
    Updates the status of the item according to checkbox selection
    """
    new_list_id = get_lists()[1]["id"] if is_checked else get_lists()[0]["id"]
    url = f"{base_trello_url}/cards/{item_id}"
    params = {
        "idList": new_list_id,
        "key" : api_key,
        "token" : token,
    }
    response = requests.put(url, params=params)
    return response
