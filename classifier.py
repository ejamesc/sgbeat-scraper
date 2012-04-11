import nltk
import re
import random
import string
from sgbeat.database import Connection
from nltk.classify.util import apply_features
from nltk.corpus import stopwords
from details import HOST_NAME

def get_bigrams_in_tweets(tweets):
    all_words = []
    [[all_words.append(c) for c in w] for w, l in tweets]
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def bigramify(tweets):
    """Convert list of tweets into lists of tuples with bigrams, loc
    """
    all_bigrams = []
    [all_bigrams.append((nltk.bigrams([c for c in w if c != ('','')]), l)) for w, l in tweets]
    #print all_bigrams
    return all_bigrams

def extract_features(document):
    document_words = set(document)
    #print document_words
    features = {}
    #print "DOCUMENT", document
    #print word_features
    for tuple in word_features:
        features['contains(%s, %s)' % tuple] = (tuple in document_words)
    return features

def filter_words(tweets):
    """Get rid of stop words, remove punctuation, and lowercase all words
    """
    res = []
    for (words, loc) in tweets:
        words_filtered = [w.lower() for w in words.split()] 
        words_filtered = [''.join(c for c in w if c not in string.punctuation) for w in words_filtered]
        words_filtered = filter(lambda x: x not in stopwords.words('english'), words_filtered)
        res.append((words_filtered, loc))
    return res


db = Connection(host = HOST_NAME,
                database = "jb_pure",
                user = "cs2102",
                password = "2012sc" 
               )

sg_users = db.query("SELECT id FROM users WHERE country='SG'")
jb_users = db.query("SELECT id FROM users WHERE country='JB'")
sg_tweets, jb_tweets = [], []
mtn = re.compile("@\w+")
hash = re.compile("#\w+")

for u in sg_users:
    curr = db.query("SELECT tweet FROM tweets WHERE user=%s", u["id"])
    curr = [hash.sub("", mtn.sub("", t['tweet'])).strip() for t in curr] # get rid of mentions
    [sg_tweets.append((t, "SG")) for t in curr]

for u in jb_users:
    curr = db.query("SELECT tweet FROM tweets WHERE user=%s", u["id"])
    curr = [hash.sub("", mtn.sub("", t['tweet'])).strip() for t in curr]
    [jb_tweets.append((t, "JB")) for t in curr]

print "Singapore", len(sg_tweets)
print "Johor", len(jb_tweets)
db.close()

#NLTK processing
tweets = []

random.shuffle(sg_tweets)
random.shuffle(jb_tweets)

tweets = bigramify(filter_words(sg_tweets + jb_tweets))
test = bigramify(filter_words(sg_tweets[:250] + jb_tweets[:250]))
#print tweets

word_features = get_word_features(get_bigrams_in_tweets(tweets))[:2000]
training_set = apply_features(extract_features, tweets)
test_set = apply_features(extract_features, test)

#Train using nltk
classifier = nltk.NaiveBayesClassifier.train(training_set)

print classifier.show_most_informative_features(32)
print "Accuracy: ", nltk.classify.accuracy(classifier, test_set)
