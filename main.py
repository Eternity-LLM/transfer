import json
from typing import Union, List

MAPPING = {}

class Message:
    def __init__(self, files:list, model:str, fragments:dict, *_, **__)->None:
        self.files = files if len(files) else None
        self.model = model
        self.msg = []
        last_msg = None
        for m in fragments:
            if m['type'] != 'SEARCH':
                content = m['content']
                if last_msg is not None:
                    content = last_msg + content
                if m['type'] == 'REQUEST':
                    self.msg.append({'role':'user', 'content':content})
                    last_msg = None
                elif m['type'] == 'THINK':
                    last_msg = f'<think>{content}</think>'
                else:
                    self.msg.append({'role':'assistant', 'content':content})
            else:
                res = ''
                for idx, site in enumerate(m['results']):
                    res += site['snippet']



class TreeNode:
    def __init__(self, id:str, parent:str, children:list, message:list, *_, **__):
        self.id = id
        self.parent = MAPPING.get(parent, None)
        self.children = [MAPPING.get(c) for c in children]
        self.message = Message(**message)
    def add_child(self, child_node:Union[str, 'TreeNode']):
        self.children.append(child_node) if isinstance(child_node, TreeNode) else MAPPING.get(child_node)
    def __getitem__(self, key):
        return self.children[key]



def load_conversations(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        conversations = json.load(file)
    #print(conversations[0])
    for c in conversations:
        pass

load_conversations('conversations.json')