from pydantic import BaseModel, ConfigDict
from peewee import *
from playhouse.shortcuts import model_to_dict
from typing import List, Union, Optional
from sqlalchemy import PrimaryKeyConstraint, String, Column, BigInteger, Text
import time
import logging

from utils.utils import decode_token
from utils.misc import get_gravatar_url

from apps.webui.internal.db import Base, JSONField, Session, get_db

import json

from config import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# Collections db Schema
####################


class Collection(Base):
    __tablename__ = 'collection'
    __table_args__ = (
        PrimaryKeyConstraint('collection_name', 'user_id'),
    )
    collection_name = Column(String)
    user_id = Column(String)


class CollectionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
    def insert_new_collection(
        self, user_id: str, collection_name:str
    ):
        with get_db() as db:

            collection = CollectionModel(
                **{
                    "collection_name": collection_name,
                    "user_id": user_id,
                }
            )
            collections_existing = db.query(Collection).filter_by(collection_name=collection_name, user_id=user_id).all()
            if len(collections_existing) == 0:
                try:
                    result = Collection(**collection.model_dump())
                    db.add(result)
                    db.commit()
                    db.refresh(result)
                    if result:
                        return True
                    else:
                        return None
                except:
                    return None
            else:
                True   
        
    def get_collections_of_user(self, user_id: str) -> List[CollectionModel]:
        try:
            with get_db() as db:
                # for result in results:
                #     print(result.collection_name)
                #     print(result.user_id)
                temp = [
                CollectionModel.model_validate(col) for col in db.query(Collection).filter_by(user_id=user_id).all()
                ]
                  
                print("Heyo")
                print(temp)
                return temp

        except Exception as e:
            print(e)
            return None

    

Collections = CollectionsTable()
