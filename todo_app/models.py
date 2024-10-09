class ListNames:
    def __init__(self):
        self.to_do = "todo"
        self.in_progress = "inprogress"
        self.done = "done"

class Item:
    def __init__(self, id, description, status = 'todo'):
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