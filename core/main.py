from typing import List

from elasticsearch import AsyncElasticsearch
from elasticsearch.client import IndicesClient
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from fastapi.responses import JSONResponse

from .models import ShipmentIn, ShipmentIndex
from elasticsearch import Elasticsearch

# from fastapi_simple_security import api_key_router, api_key_security

# DATABASE CONNECTION
client = MongoClient("mongodb", 27017)

# initialize fastAPI 
app = FastAPI()

# Authentication
# app.include_router(api_key_router, prefix="/auth", tags=["_auth"])

# call AsyncElasticsearch to establish connection
es = AsyncElasticsearch(["localhost"], port=9200)

# index class object
index = IndicesClient(es)




# MIDDLEWARE
# ----------------------------------------------------------------------------------------------
# cors middleware

# define the origin servers to allow
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def parse_document(search_word, id, limit, offset):
    body = {
        "from": offset,
        "size": limit,
        "sort": [{"id": "desc"}, "_score"],
        "query": {
            "bool": {
                "filter": {"term": {"business_id_id": id}},
                "must": {"query_string": {"query": f"*{search_word}*"}},
            }
        },
        "highlight": {
            "pre_tags": "<em>",
            "post_tags": "</em>",
            "fields": {"*": {}},
            "tags_schema": "styled",
        },
    }
    return body


# shipment APIs
# ------------------------------------------------------------------------------------------------------------

# search shipments
@app.get("/shipment/search/{business_id}/{search_word}/", response_model=List[ShipmentIndex])
async def search_shipments(
    search_word: str, business_id: int, limit: int = 50, offset: int = 0
):
    doc = parse_document(
        search_word=search_word, id=business_id, limit=limit, offset=offset
    )
    deleted_index = index.delete(index="shipments")
    print(f"************************{deleted_index}**********************")
    res = await es.search(index="shipments", body=doc)
    return JSONResponse(status_code=status.HTTP_200_OK, content=res['hits']['hits'])


# carrier agents APIs
# -------------------------------------------------------------------------------------------------------------

# search carrier agents
# @app.get("/carriers_agents/search/{business_id}/{search_word}/", dependencies=[Depends(api_key_security)])
@app.get("/carriers_agents/search/{business_id}/{search_word}/")
async def search_carrier_agents(
    search_word: str, business_id: int, limit: int = 50, offset: int = 0
):
    doc = await parse_document(
        search_word=search_word, id=business_id, limit=limit, offset=offset
    )
    response = await es.search(index="carrier_agents", body=doc)
    return response


# carrier APIs
# -------------------------------------------------------------------------------------------------------------

# search carriers
# @app.get("/carriers/search/{business_id}/{search_word}/", dependencies=[Depends(api_key_security)])
@app.get("/carriers/search/{business_id}/{search_word}/")
async def search_carriers(
    search_word: str, business_id: int, limit: int = 50, offset: int = 0
):
    doc = await parse_document(
        search_word=search_word, id=business_id, limit=limit, offset=offset
    )
    response = await es.search(index="carriers", body=doc)
    return response


# email_threads APIs
# --------------------------------------------------------------------------------------------------------------

# search threads
# @app.get("/threads/search/{business_id}/{search_word}/", dependencies=[Depends(api_key_security)])
# @app.get("/threads/search/{business_id}/{search_word}/")
async def search_threads(
    search_word: str, business_id: int, limit: int = 50, offset: int = 0
):
    doc = await parse_document(
        search_word=search_word, id=business_id, limit=limit, offset=offset
    )
    response = await es.search(index="threads", body=doc)
    return response


# business users APIs
# ---------------------------------------------------------------------------------------------------------------

# search users
# @app.get("/business_users/search/{business_id}/{search_word}/", dependencies=[Depends(api_key_security)])
@app.get("/business_users/search/{business_id}/{search_word}/")
async def search_users(
    search_word: str, business_id: int, limit: int = 50, offset: int = 0
):
    doc = await parse_document(
        search_word=search_word, id=business_id, limit=limit, offset=offset
    )
    res = await es.search(index="business_users", body=doc)
    return res


# pointer setup
# create a table and setup initial values as one or default values point to index 1
# now if we point to index 1 search for index 2 
# ------ if index 2 is present drop it and create new index
# ------ update the table pointer points to 2.

# find the index with given name if we found the index
# use delete api to delete the whole index  
# then use create index api to recreate the new whole index
# -> update the newly create index name(value) in sql table