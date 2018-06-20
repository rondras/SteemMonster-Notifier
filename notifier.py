from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post
import json
import datetime

user = "yourusername"
steem = Steem(keys=['POSTINGKEY','ACTVEKEY'])


def converter(object_):
    if isinstance(object_, datetime.datetime):
        return object_.__str__()

def stream_blockchain():
    blockchain = Blockchain()
    stream = blockchain.stream(filter_by=['custom_json'])
    while True:
        try:
            for custom_json  in stream:
                data = custom_json["json"]
                author = custom_json["required_posting_auths"][0]
                parsed_json = json.loads(data)
                code = custom_json["id"]

                if author == "steemmonsters" and code == "generate_packs":
                     account = parsed_json["account"]
                     print (account)
                     packs = parsed_json["packs"]
                     cards = packs[0][1]
                     for card in cards:
                         monstercode = card[0]
                         cardcode = card[1]
                         print (monstercode)
                         print (cardcode)
                         if monstercode == 56 and cardcode.startswith("G"):
                             text = "Golden Selenia Sky card was created and transferred to " + account
                             steem.transfer(user, amount=0.001, asset="SBD", memo=text, account=user)

        except Exception as error:
            print(repr(error))
            continue

if __name__ == '__main__':
    stream_blockchain()
