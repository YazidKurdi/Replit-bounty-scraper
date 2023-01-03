import os
from pymongo import MongoClient
import pandas as pd
from scrape import scrape_bounties

# establish a client connection
MONGODB_CONNECTION_STRING = os.environ['MONGODB_CONNECTION_STRING']
client = MongoClient(MONGODB_CONNECTION_STRING)

