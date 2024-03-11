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

class TrelloService():

    def __init__(self):
        self.board_id = os.getenv('TRELLO_BOARD_ID')
        self.api_key = os.getenv("TRELLO_API_KEY")
        self.token = os.getenv("TRELLO_TOKEN")
        self.base_trello_url = "https://api.trello.com/1"

    def get_lists(self):
        """
        Returns all the lists on the trello board
        """
        url = f"{self.base_trello_url}/boards/{self.board_id}/lists"
        params = {
            "key" : self.api_key,
            "token" : self.token
        }

        response = requests.get(url, params=params)
        response_json = response.json()

        return response_json

    def get_list(self, list_id):
        """
        Returns a list of a given ID
        """
        url = f"{self.base_trello_url}/list/{list_id}"
        params = {
            "key" : self.api_key,
            "token" : self.token
        }

        response = requests.get(url, params=params)
        response_json = response.json()

        return response_json

    def get_items(self):
        """
        Fetches all items on the trello board
        """
        url = f"{self.base_trello_url}/boards/{self.board_id}/cards"
        params = {
            "key" : self.api_key,
            "token" : self.token
        }

        response = requests.get(url, params=params)
        response_json = response.json()

        list_refs = self.get_lists()
        lists = {}
        for list in list_refs:
            lists[list['id']] = self.get_list(list['id'])

        items = []
        for card in response_json:
            item = Item.from_trello_card(card, lists[card["idList"]])
            items.append(item)

        return items

    def get_item(self, id):
        """
        Fetches the item with the specified ID.
        """
        items = self.get_items()
        return next((item for item in items if item['id'] == int(id)), None)


    def add_item(self, title):
        """
        Adds a new item with the specified title to the list.
        """
        list_id = self.get_lists()[0]["id"]
        url = f"{self.base_trello_url}/cards"
        params = {
            "idList": list_id,
            "key" : self.api_key,
            "token" : self.token,
            "name" : title
        }

        response = requests.post(url, params=params)

        return response

    def update_status(self, item_id, is_checked):
        """
        Updates the status of the item according to checkbox selection
        """
        new_list_id = self.get_lists()[1]["id"] if is_checked else self.get_lists()[0]["id"]
        url = f"{self.base_trello_url}/cards/{item_id}"
        params = {
            "idList": new_list_id,
            "key" : self.api_key,
            "token" : self.token,
        }
        response = requests.put(url, params=params)
        return response
