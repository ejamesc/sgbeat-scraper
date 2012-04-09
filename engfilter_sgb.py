import cld
import re
from sgbeat.database import Connection
from details import (
    USERNAME,
    PASSWORD,
    HOST_NAME,
    MYSQL_USER_NAME,
    MYSQL_PASSWORD
)

db = Connection(host = HOST_NAME,
                database = "sgbeat",
                user = MYSQL_USER_NAME,
                password = MYSQL_PASSWORD
               )
db2 = Connection(host = HOST_NAME,
                 database = "sgb_pure",
                 user = "cs2102",
                 password = "2012sc" 
                )

tweets = db.query("SELECT * FROM tweets")
count = 0
for t in tweets:
    c = t["tweet"].encode('utf-8')
    # language detection
    name, code, reliable, bytes_found, details = cld.detect(c)
    # compile a regex for urls. We don't want tweets with urls
    r = re.compile(r"(http://[^ ]+)")
    urlmatch = r.search(c)
    # we use a set to save tweets, and check against that to prevent duplicates
    saved = set()
    if (code == "en" or code == "un") and not urlmatch and c not in saved:
        # we allow 'unknown' languages into our database, as these are mostly short singlish sentences
        db2.execute("INSERT INTO tweets (user, tweet) VALUES (%s, %s)", t["user"], c)
        saved.add(c)
    else:
        print "Not English: " + c + " lang:" + name
        count = count + 1

db.close()
db2.close()
print "Not English: " 
print count


