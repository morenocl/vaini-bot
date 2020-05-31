from pymongo import MongoClient
from collections import defaultdict
from telegram.ext import BasePersistence
from dotenv import load_dotenv
import os


class MongodbPersistence(BasePersistence):

    def __init__(self,
                 store_user_data=True,
                 store_chat_data=True,
                 store_bot_data=True,
                 on_flush=False):
        super(MongodbPersistence, self).__init__(store_user_data=store_user_data,
                                                store_chat_data=store_chat_data,
                                                store_bot_data=store_bot_data)
        self.user_data = defaultdict(int)
        self.chat_data = defaultdict(dict)
        self.bot_data = defaultdict(dict)
        self.conversations = defaultdict(dict)
        load_dotenv()
        self.db_user = os.getenv('DB_USER')
        self.db_pass = os.getenv('DB_PASS')
        self.db_name = os.getenv('DB_NAME')


    def open_db(self):
        try:
            self.client = MongoClient('mongodb://'+self.db_user+':'+self.db_pass+'@dbh63.mlab.com:27637/'+self.db_name+'?retryWrites=false')
        except:
            print("Error while connecting to mongo")
        return self.client[self.db_name]

    def close_db(self):
        if self.client:
            self.client.close()

    def get_bot_data(self):
        print('get_bot_data()')
        return self.bot_data

    def get_chat_data(self):
        print('get_chat_data()')
        return self.chat_data

    def get_user_data(self):
        print('get_user_data()')
        collection = self.open_db().user_data
        data = collection.find()
        for d in data:
            self.user_data[d['user_id']] = d['lista']
        self.close_db()
        return self.user_data

    def get_conversations(self, name):
        print('get_conversations()', name)
        return self.conversations

    def update_bot_data(self, data):
        print('update bot data:', data)

    def update_chat_data(self, chat_id, data):
        print('update chat data:', chat_id, data)

    def update_user_data(self, user_id, data):
        print('update user data:', user_id, defaultdict(int) if not data else data)
        doc = {"user_id": user_id, "lista": defaultdict(int) if not data else data}
        collection = self.open_db().user_data
        collection.replace_one({"user_id": user_id}, doc, upsert=True)
        self.close_db()

    def update_conversation(self, name, key, new_state):
        print('Update conversations:', name, key, new_state)

    def flush(self):
         print('flush()')
