from __future__ import print_function

import random
from random import choices 
import emoji 
from emoji.unicode_codes import UNICODE_EMOJI
import argparse, json, pprint, requests, sys, urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode


SEARCH_LIMIT = 3

with open("config.json", "r") as f:
    data = json.load(f)
API_KEY = data['api_key']
API_HOST = data["API_HOST"]
SEARCH_PATH = data["SEARCH_PATH"]
BUSINESS_PATH = data["BUSINESS_PATH"]
    
    
def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    response = requests.request('GET', url, headers=headers, params=url_params)    
    return response.json()


def search(api_key, term, latitude, longitude):
    #Query the Search API by a search term and location.
    url_params = {
        'term': term.replace(' ', '+'),
        'latitude': latitude, 
        'longitude': longitude, 
        'limit': SEARCH_LIMIT

    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    #Query the Business API by a business ID.
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)


#Queries the API by the input values from the user.
def query_api(term,latitude, longitude):
    try: 
        response = search(API_KEY, term, latitude, longitude)
        businesses = response.get('businesses')
        if not businesses:
            print(u'No businesses for {0} in {1} found.'.format(term, location))
            ask_for_emoji()
         
        response = get_business(API_KEY, businesses[0]['id'])
        response2 = get_business(API_KEY, businesses[1]['id'])
        response3 = get_business(API_KEY, businesses[2]['id'])
        print(u'Result for business "{0}" found:'.format(businesses[0]['name']))
        print(u'Result for business "{0}" found:'.format(businesses[1]['name']))
        print(u'Result for business "{0}" found:'.format(businesses[2]['name']))
        pprint.pprint(response, indent=2)
        print('')
        pprint.pprint(response2, indent=2)
        print('')
        pprint.pprint(response3, indent=2)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
                )
            )
        
        

def ask_for_emoji():
    MAIN_QS = ["What do you fancy today?", "What food are you feeling?"]
    emojis_list = [":pizza:",":ice_cream:", ":sushi:", ":spaghetti:", ":sake:", ":french_fries:", ":curry_rice:", ":doughnut:", ":Vietnam:", ":United_States:", ":Italy:", ":China:", ":United_Kingdom:", ":Chile:", ":Egypt:"]
    new_list = []
    for i in emojis_list:
        new_list.append(emoji.emojize(i))
    print(new_list)         
    sentence = input()
    print("Hi there!")
    sentence = input(random.choice(MAIN_QS) + str(random.sample(new_list, 3)))
    
    if sentence in emoji.UNICODE_EMOJI:
        emoji_input = str(sentence)
        #gets text of emoji
        text = UNICODE_EMOJI[emoji_input]
        #saves text without colons
        TERM = text[1:len(text)-1]
        LOCATION = input("location?")
        locations = ['near me', 'current location', 'here', 'around me', 'around here', 'current']
        if LOCATION.lower() in locations: 
            import geocoder
            g = geocoder.ip('me')
            #only finds your city and state...try latlng
            query_api(TERM,g.latlng[0], g.latlng[1])
        else: 
            query_api(TERM, LOCATION)       
    else:
        print("Sorry, I only accept emojis" + ' ' + emoji.emojize(':crying_face:'))
        ask_for_emoji()


ask_for_emoji()


'''emoji chart 
https://unicode.org/emoji/charts/full-emoji-list.html '''

'''import geocoder
g = geocoder.ip('me')
print(g.latlng)'''