import os

class ListNames:
    def __init__(self):
        self.to_do = os.getenv("TO_DO_LIST_NAME")
        self.in_progress = os.getenv("IN_PROGRESS_LIST_NAME")
        self.done = os.getenv("DONE_LIST_NAME")

class Item:
    def __init__(self, id, name, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], list.name)
    
class List:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def from_trello_list(cls, list):
        return cls(list['id'], list['name'])

class ViewModel:
    def __init__(self, items, lists):
        self._items = items
        self._lists = lists
        self._list_names = ListNames()
 
    @property
    def items(self):
        return self._items
    
    @property
    def lists(self):
        return self._lists
    
    @property
    def done_items(self):
        return [item for item in self._items if item.status == self._list_names.done]
    
    @property
    def todo_items(self):
        return [item for item in self._items if item.status == self._list_names.to_do]
    
    @property
    def inprogress_items(self):
        return [item for item in self._items if item.status == self._list_names.in_progress]