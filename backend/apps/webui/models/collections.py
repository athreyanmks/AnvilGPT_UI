from pydantic import BaseModel
from peewee import *
from playhouse.shortcuts import model_to_dict
from typing import List, Union, Optional
import time
import logging

from utils.utils import decode_token
from utils.misc import get_gravatar_url

from apps.webui.internal.db import DB

import json

from config import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# Collections DB Schema
####################


class Collection(Model):
    collection_name = CharField()
    user_id = CharField()

    class Meta:
        database = DB


class CollectionModel(BaseModel):
    collection_name: str
    user_id: str


####################
# Forms
####################


class CollectionResponse(BaseModel):
    collection_name: str
    user_id: str
    type : str
    title : str
    name : str
    collection_names : List[str]


# class DocumentUpdateForm(BaseModel):
#     name: str
#     title: str


# class CollectionsForm(BaseModel):
#     collection_name: str
#     user_id: str


class CollectionsTable:
    def __init__(self, db):
        self.db = db
        self.db.create_tables([Collection])

    def insert_new_collection(
        self, user_id: str, collection_name:str
    ):
        document = CollectionModel(
            **{
                "collection_name": collection_name,
                "user_id": user_id,
            }
        )

        collections = Collection.select().where((Collection.collection_name == collection_name) & (Collection.user_id == user_id))
        if len(collections) == 0:
            try:
                # print("Here6")
                result = Collection.create(**document.model_dump())
                # print(result)
                # print("########")
                if result:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False    
        
    def get_collections_of_user(self, user_id: str) -> List[CollectionModel]:
        # try:
            results  = Collection.select()
            # for result in results:
            #     print(result.collection_name)
            #     print(result.user_id)
            temp =  [
            CollectionModel(**model_to_dict(collection))
            for collection in Collection.select().where(Collection.user_id == user_id)
            ]
            # print("Heyo")
            # print(temp)
            return temp

        # except:
        #     return None

    

Collections = CollectionsTable(DB)
