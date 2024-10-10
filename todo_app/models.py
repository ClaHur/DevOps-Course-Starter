from todo_app.assets.constants import todo_status, in_progress_status, done_status

class ListNames:
    def __init__(self):
        self.to_do = todo_status
        self.in_progress = in_progress_status
        self.done = done_status

class Item:
    def __init__(self, id, description, status = todo_status):
        self.id = id
        self.description = description
        self.status = status
    
class List:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class ViewModel:
    def __init__(self, items):
        self._items = items
        self._list_names = ListNames()
 
    @property
    def items(self):
        return self._items
    
    @property
    def done_items(self):
        return [item for item in self._items if item.status == self._list_names.done]
    
    @property
    def todo_items(self):
        return [item for item in self._items if item.status == self._list_names.to_do]
    
    @property
    def inprogress_items(self):
        return [item for item in self._items if item.status == self._list_names.in_progress]