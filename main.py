import json
from typing import Union, List

MAPPING = {}
with open('search_prompt.txt', mode='r', encoding='utf-8') as f:
    SEARCH_PROMPT = f.read()

class Message:
    def __init__(self, files:list, model:str, fragments:dict, inserted_at:str,*_, **__)->None:
        self.files = files if len(files) else None
        self.model = model
        self.msg = []
        self.date = inserted_at[:10]
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
                for idx, site in enumerate(m['results'], start=1):
                    res += f'[webpage {idx} begin]\\n来自 {site['site_name']} {site['url']}\\n{site['snippet']}\\n[webpage {idx} end]'
                res += f'\\n{SEARCH_PROMPT}\\n' + f'- 今天是{self.date}'
                self.msg.append({'role':'system', 'content':''})
                if self.msg[-2]['role']=='user':
                    self.msg[-1]['content'] = f'以下内容是基于用户的问题的搜索结果：\\n{res}'
                    self.msg.append(self.msg.pop(-2))
                else:
                    self.msg[-1]['content'] = f'以下内容是系统搜索结果：\\n{res}'

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