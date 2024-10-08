from todo_app.models import Item, List, ViewModel

to_do_list_name = "todo"
done_list_name = "done"
in_progress_list_name = "in_progress"

def test_done_items_property_lists_all_done_items(monkeypatch):
    # Arrange
    to_do_item_1 = Item(1,"ToDo1",to_do_list_name)
    in_progress_item_1 = Item(2,"InProgress1",in_progress_list_name)
    done_item_1 = Item(3,"Done1",done_list_name) 
    done_item_2 = Item(4,"Done2",done_list_name) 

    items = [to_do_item_1, in_progress_item_1, done_item_1, done_item_2]
    lists = [List(1,to_do_list_name), List(2, done_list_name)]
    view_model = ViewModel(items, lists)

    # Act
    done_items = view_model.done_items

    # Assert
    assert to_do_item_1 not in done_items
    assert in_progress_item_1 not in done_items
    assert done_item_1 in done_items
    assert done_item_2 in done_items

def test_todo_items_property_lists_all_done_items(monkeypatch):
    # Arrange
    to_do_item_1 = Item(1,"ToDo1",to_do_list_name)
    to_do_item_2 = Item(2,"ToDo2",to_do_list_name)
    in_progress_item_1 = Item(2,"InProgress1",in_progress_list_name) 
    done_item_1 = Item(3,"Done1",done_list_name) 

    items = [to_do_item_1, in_progress_item_1, to_do_item_2, done_item_1]
    lists = [List(1,to_do_list_name), List(2, done_list_name)]
    view_model = ViewModel(items, lists)

    # Act
    todo_items = view_model.todo_items

    # Assert
    assert to_do_item_1 in todo_items
    assert to_do_item_2 in todo_items
    assert in_progress_item_1 not in todo_items
    assert done_item_1 not in todo_items


def test_todo_items_property_lists_all_done_items(monkeypatch):
    # Arrange
    to_do_item_1 = Item(1,"ToDo1",to_do_list_name)
    in_progress_item_1 = Item(2,"InProgress1",in_progress_list_name) 
    in_progress_item_2 = Item(2,"InProgress2",in_progress_list_name) 
    done_item_1 = Item(3,"Done1",done_list_name) 

    items = [to_do_item_1, in_progress_item_1, in_progress_item_2, done_item_1]
    lists = [List(1,to_do_list_name), List(2, done_list_name)]
    view_model = ViewModel(items, lists)

    # Act
    inprogress_items = view_model.inprogress_items

    # Assert
    assert in_progress_item_1 in inprogress_items
    assert in_progress_item_1 in inprogress_items
    assert to_do_item_1 not in inprogress_items
    assert done_item_1 not in inprogress_items