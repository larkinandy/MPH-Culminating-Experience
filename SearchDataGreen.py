# SearchDataGreen.py #
# Created by Andrew Larkin
# Date created: December 7th, 2016
# Created for culminating experience project as part of fulfining 
# MPH requirements at George Washington University
# This script downloads tweets from Twitter containing select keywords and stores them in an SQL database.

# note: some of the code in this script is based on open source code available at:
# http://stackoverflow.com/questions/16867504/tweepy-streaming-api-returning-none-for-coordinates-on-geo-enabled-tweets

import json
import tweepy
import dataset

access_token = # insert personal access token 
access_token_secret = # insert personal token secret 
consumer_key = # insert consumer key 
consumer_secret = # insert consumer secret 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

SQL_DATABASE = # inesrt filepath to SQL database - make sure the file extension is .db.  Example: "C://myDatabase.db"
CSV_NAME = "tweets.csv"
databaseName = "greenTweets"

db = dataset.connect(SQL_DATABASE)
CONNECTION_STRING = SQL_DATABASE

searchTerms = ['park','parks','tree' 'trees','nature','bush','bushes','grass','flower','flowers','plant','plants',
               'garden','yard','backyard','leaves','forest','trail','mountain','lawn','field','crop','hay',
               'prarie','pasture','lake','lakes','river','rivers','riverside','stream','streams']


# customize a listener to only store data of interest
class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        created = status.created_at
        if coords is not None:
            coords = json.dumps(coords)
        table = db[databaseName]
        table.insert(dict(
            user_location=loc,
            coordinates=coords,
            text=text,
            created=created
            ))

    def on_error(self, status_code):
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream

def dumpData():
    db = dataset.connect(SQL_DATABASE)
    result = db[databaseName].all()
    dataset.freeze(result, format='csv', filename=CSV_NAME)
    print("completed dump of SQL database to csv file")


def main():
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
    sapi.filter(track=searchTerms)

main()