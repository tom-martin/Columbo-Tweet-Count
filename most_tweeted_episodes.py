import urllib
import urllib2
import json
import time


f = open('columbo_episodes.txt', 'r')

def get_tweet_count(term):
    total_tweet_count = 0
    max_id = None
    page = 1
    while True:
        url = 'http://search.twitter.com/search.json?q=' + urllib.quote(term) + '&rpp=100&page=' + str(page)

        if max_id:
            url += '&max_id=' + max_id

        response = urllib2.urlopen(url)
        json_content = response.read()

        
        tweets = json.loads(json_content)['results']

        total_tweet_count += len(tweets)

        # Are we at the last page or have we run out of pages?
        if len(tweets) < 100 or page >= 15:
            break

        max_id = tweets[0]['id_str']
        page += 1

        # Wait so twitter doesn't get annoyed with us
        time.sleep(1)

    return total_tweet_count

episodes = []

for episode in f:
    try:
        episodes.append({'name' : episode.strip(), 'tweet_count' : get_tweet_count('"' + episode.strip() + '" columbo')})
    except Exception as e:
        print 'Exception when getting tweet count for ' + episode.strip()
        print str(e)

episodes.sort(key=lambda e : e['tweet_count'], reverse=True)

for episode in episodes:
    print episode['name'] + '|' + str(episode['tweet_count'])


        
