import requests
import os

from todo_app.models import Item, List, ListNames

class TrelloService():

    def __init__(self):
        self.board_id = os.getenv('TRELLO_BOARD_ID')
        self.api_key = os.getenv("TRELLO_API_KEY")
        self.token = os.getenv("TRELLO_TOKEN")
        self.base_trello_url = "https://api.trello.com/1"
        self.list_names = ListNames()
        self.lists_cache = None

    def get_lists(self):
        """
        Returns all the lists on the Trello board
        """
        if self.lists_cache is None:
            self.lists_cache = self.fetch_lists_from_api()
        return self.lists_cache
        

    def fetch_lists_from_api(self):
        url = f"{self.base_trello_url}/boards/{self.board_id}/lists"
        params = {
            "key" : self.api_key,
            "token" : self.token
        }

        response = requests.get(url, params=params)
        response_json = response.json()

        lists = []
        for list in response_json:
            list_details = List(list["id"], list["name"])
            lists.append(list_details)

        return lists

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

        return List.from_trello_list(response_json)

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

        items = []
        for card in response_json:
            item = Item.from_trello_card(card, self.get_list_by_id(card["idList"]))
            items.append(item)

        return items

    def get_item(self, id):
        """
        Fetches the item with the specified ID.
        """
        url = f"{self.base_trello_url}/cards/{id}"
        params = {
            "key" : self.api_key,
            "token" : self.token
        }

        response = requests.get(url, params=params)
        response_json = response.json()

        return response_json


    def add_item(self, item_name):
        """
        Adds a new item with the specified title to the list.
        """
        list_id = self.get_list_by_name(self.list_names.to_do).id
        url = f"{self.base_trello_url}/cards"
        params = {
            "idList": list_id,
            "key" : self.api_key,
            "token" : self.token,
            "name" : item_name
        }

        response = requests.post(url, params=params)

        return response
    
    def update_status(self, item_id, new_status):
        """
        Updates the status of the item according to the provided status
        """
        new_list_id = self.get_list_by_name(new_status).id
        url = f"{self.base_trello_url}/cards/{item_id}"
        params = {
            "idList": new_list_id,
            "key" : self.api_key,
            "token" : self.token,
        }

        response = requests.put(url, params=params)

        return response
    
    def delete_item(self, item_id):
        """
        Deletes completed cards
        """
        url = f"{self.base_trello_url}/cards/{item_id}"
        params = {
            "key" : self.api_key,
            "token" : self.token,
        }

        response = requests.delete(url, params=params)
        
        return response
    
    def get_list_by_name(self, name_to_search):
        lists = self.get_lists()
        for list in lists:
            if list.name == name_to_search:
                return list
        return None 
    
    def get_list_by_id(self, id_to_search):
        lists = self.get_lists()
        for list in lists:
            if list.id == id_to_search:
                return list
        return None 
