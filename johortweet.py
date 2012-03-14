#!/usr/bin/env python
"""Use Twitter's streaming API to grab tweets.
"""

import tweetstream
from sgbeat.database import Connection
from details import (
            USERNAME,
            PASSWORD,
            HOST_NAME,
            MYSQL_DB_NAME,
            MYSQL_USER_NAME,
            MYSQL_PASSWORD
        )

#note that coordinate pairs are long/lat not lat/long
#Singapore coordinates
#locations = ["103.61,1.22","104.01356,1.456674"]

#Johor coordinates
locations = ["103.55,1.45", "103.87,1.63"]

with tweetstream.FilterStream(
                USERNAME,
                PASSWORD,
                locations=locations) as stream:
    for tweet in stream:
        db = Connection(host = HOST_NAME,
                        database = MYSQL_DB_NAME,
                        user = MYSQL_USER_NAME,
                        password = MYSQL_PASSWORD
                )
        username = tweet["user"]["screen_name"]
        text = tweet["text"]
        loc = tweet["place"]["full_name"]

        user = db.get("SELECT id FROM users WHERE username=%s", username)
        if user:
            db.execute("INSERT into tweets (user, tweet, location) VALUES (%s, %s, %s)", user["id"], text, loc)
        else:
            db.execute("INSERT into users (username) VALUES (%s)", username)
            user = db.get("SELECT id FROM users WHERE username=%s", username)
            db.execute("INSERT into tweets (user, tweet, location) VALUES (%s, %s, %s)", user["id"], text, loc)

        db.close()

        #print "==================="
        #print text
        #print username
        #print "(%s)" % loc

