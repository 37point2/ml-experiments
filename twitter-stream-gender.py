import tweepy
import json
import sys
import nlp

api_keys = json.load(open('api/api.json', 'r'))

CONSUMER_KEY = api_keys['api']['twitter']['CONSUMER_KEY']
CONSUMER_SECRET = api_keys['api']['twitter']['CONSUMER_SECRET']
ACCESS_TOKEN = api_keys['api']['twitter']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = api_keys['api']['twitter']['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

gender_mappings = [x.replace('\n','').split(',')[1:] for x in open('corpora/gender.top100.1to3grams.csv').readlines()[2:]]

gender_mappings_dict = {}
for mapping in gender_mappings:
    gender_mappings_dict[mapping[0]] = (mapping[1], mapping[2])

#print gender_mappings_dict

class StreamListener(tweepy.StreamListener):
        def on_status(self, tweet):
            print 'Ran on_status'

        def on_error(self, status_code):
            print 'Error: ' + repr(status_code)
            return False

        def on_data(self, data):
            try:
                json_data = json.loads(data)
                if not json_data.has_key("friends"):
                    screen_name = json_data["user"]["screen_name"]
                    text = json_data["text"]
                    gender = determine_gender(text)
                    #if gender != "unknown":
                    print screen_name + ", " + gender + ": " + text + "\n"
            except:
                pass

def determine_gender(text):
    features = []
    [features.append(x) for x in text.split(' ')]
    #[features.append(x) for x in nlp.bigrams(text, exclude=None, freq=0, limit=0)]
    #[features.append(x) for x in nlp.trigrams(text, exclude=None, freq=0, limit=0)]

    score = 0

    #dumb scoring algorithm below

    for feature in features:
        if isinstance(feature, list):
            phrase = ' '.join(feature)
        else:
            phrase = feature
        #print phrase
        if gender_mappings_dict.has_key(phrase):
            score += float(gender_mappings_dict[phrase][0])

    #print score

    if score > 0:
        return "female"
    elif score < 0:
        return "male"
    else:
        return "unknown"

def stream(args):
    listener = StreamListener()
    streamer = tweepy.Stream(auth=auth, listener=listener)
    streamer.userstream()

def main(args):
    stream(args)
    #print determine_gender("nfl fifa beard nba halo modern warfare")

if __name__ == '__main__':
    main(sys.argv[1:])