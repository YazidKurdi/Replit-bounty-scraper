from scrape import scrape_bounties
from mongo import client
from pandas import read_csv

if __name__ == "__main__":
    scrape_bounties()
    bounties_dict = read_csv("bounties.csv").to_dict("records")

    # point to symbolsDB collection
    db = client.bountiesDB
    # emtpy symbols collection before inserting new records
    db.bountiesDB.drop()
    # insert new symbols
    db.bountiesDB.insert_many(bounties_dict)