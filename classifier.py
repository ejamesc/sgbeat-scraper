import nltk
import random
from sgbeat.database import Connection
from details import HOST_NAME

db = Connection(host = HOST_NAME,
                 database = "jb_pure",
                 user = "cs2102",
                 password = "2012sc" 
                )

sg_users = db.query("SELECT id FROM users WHERE country='SG'")
jb_users = db.query("SELECT id FROM users WHERE country='JB'")
sg_tweets = []
jb_tweets = []

for u in sg_users:
    curr = db.query("SELECT tweet FROM tweets WHERE user=%s", u["id"])
    [sg_tweets.append(( t['tweet'], "SG")) for t in curr]

for u in jb_users:
    curr = db.query("SELECT tweet FROM tweets WHERE user=%s", u["id"])
    [jb_tweets.append(( t['tweet'], "JB")) for t in curr]



print len(sg_tweets)
print len(jb_tweets)

db.close()
