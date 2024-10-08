import os
from dotenv import find_dotenv, load_dotenv


file_path = find_dotenv('.env.test')
load_dotenv(file_path, override=True)

class TestData:
    fake_to_do_list_id = '123abc'
    fake_in_progress_list_id = "456def"
    fake_done_list_id = "789ghi"

    fake_to_do_card = {'id': '123', 'name': 'To Do Card', 'idList': fake_to_do_list_id}
    fake_in_progress_card = {'id': '456', 'name': 'In Progress Card', 'idList': fake_in_progress_list_id}
    fake_done_card = {'id': '789', 'name': 'Done Card', 'idList': fake_done_list_id}

    fake_cards = [fake_to_do_card, fake_in_progress_card, fake_done_card]

    fake_to_do_list = {
            'id': fake_to_do_list_id,
            'name': 'todo',
            'cards': [fake_to_do_card]
        }
    
    fake_in_progress_list = {
            'id': fake_in_progress_list_id,
            'name': 'inprogress',
            'cards': [fake_in_progress_card]
        }

    fake_done_list = {
            'id': fake_done_list_id,
            'name': 'done',
            'cards': [fake_done_card]
        }
       
    fake_lists = [fake_to_do_list, fake_in_progress_list, fake_done_list]