import requests
import csv
import json
import time
import calendar
import datetime 

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


vader = SentimentIntensityAnalyzer()



def fetch_data(query, after_ts, before_ts, subreddit):
    url = "https://api.pushshift.io/reddit/search/submission/?q="+str(query[0])+"&size=10000&after="+str(after_ts)+"&before="+str(before_ts)+"&subreddit="+str(subreddit)
    r = requests.get(url)
    data = json.loads(r.text)
    return data["data"]



def fetch_submission_data(submission, writer):
        
    if "removed_by_category" in submission:
        return None
    if "selftext" not in submission:
        return None
    if submission["selftext"] == "[removed]" or submission["selftext"] == "":
        return None
    
    writer.writerow({"id": submission["id"],
                     "score": submission["score"],
                     "date": datetime.datetime.fromtimestamp(submission["created_utc"]),
                     "body_sentiment": vader.polarity_scores(submission["selftext"])["compound"],
                     "title_sentiment": vader.polarity_scores(submission["title"])["compound"]})



def main():
    
    before_ts = calendar.timegm(datetime.datetime.now().timetuple())
    after_ts = calendar.timegm(datetime.datetime(2020, 4, 1).timetuple())   
    subreddit = "wallstreetbets"
    query = ["GME", "GameStop"]
    
    existing = input("Did you check if there was an existing file? ")
    if existing != "y":
        return
    
    db = open("db.csv", "a")
    fieldnames = ["id", "score", "date", "body_sentiment", "title_sentiment"]
    writer = csv.DictWriter(db, fieldnames=fieldnames)
    writer.writeheader()
    
    data = fetch_data(query, after_ts, before_ts, subreddit)
    
    counter = 0
    while len(data) > 0:
        for submission in data:
            counter += 1
            fetch_submission_data(submission, writer)
        
        print(f"Posts analyzed {counter}; Size of data: {len(data)}; Last timestamp: {datetime.datetime.fromtimestamp(data[-1]['created_utc'])}")
        after_ts = data[-1]["created_utc"]
        
        
        data = fetch_data(query, after_ts, before_ts, subreddit)
        
    db.close()
    
    

if __name__ == "__main__":
    main()
