from __future__ import print_function

import random
from random import choices 
import emoji 
from emoji.unicode_codes import UNICODE_EMOJI

import argparse, json, pprint, requests, sys, urllib

try:

    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode

except ImportError:

    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode
    

API_KEY= "yNvU5hJ2u4gBpIzmdeKzClCz0vizVcSu5_H9PbbhAz5ExSghk793K8pOCDlhG7kfK0LbRGWMm1G2GMUmTxJD2aFt8PWOB3C6KyFC02eYWDr7p-BvN7Bygwj7TGvuWnYx"
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
SEARCH_LIMIT = 3

def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    response = requests.request('GET', url, headers=headers, params=url_params)    
    return response.json()

def search(api_key, term, location):
    #Query the Search API by a search term and location.
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT

    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

def get_business(api_key, business_id):
    #Query the Business API by a business ID.
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)

#Queries the API by the input values from the user.
def query_api(term, location):

    response = search(API_KEY, term, location)
    businesses = response.get('businesses')
    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        ask_for_emoji()
    business_id1 = businesses[0]['id']
    business_id2 = businesses[1]['id']
    business_id3 = businesses[2]['id']
    response = get_business(API_KEY, business_id1)
    response2 = get_business(API_KEY, business_id2)
    response3 = get_business(API_KEY, business_id3)
    print(u'Result for business "{0}" found:'.format(businesses[0]['name']))
    print(u'Result for business "{0}" found:'.format(businesses[1]['name']))
    print(u'Result for business "{0}" found:'.format(businesses[2]['name']))
    pprint.pprint(response, indent=2)
    print('')
    pprint.pprint(response2, indent=2)
    print('')
    pprint.pprint(response3, indent=2)

def main(input_term, input_location):
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--term', dest='term', default=input_term,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=input_location, type=str,
                        help='Search location (default: %(default)s)')
    input_values = parser.parse_args()
    try:
        query_api(input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )
MAIN_QS = ["What do you fancy today?", "What food are you feeling?"]
emojis_list = [":pizza:",":ice_cream:", ":sushi:", ":spaghetti:", ":sake:", ":french_fries:", ":curry_rice:", ":doughnut:", ":Vietnam:", ":United_States:", ":Italy:", ":China:", ":United_Kingdom:", ":Chile:", ":Egypt:"]
new_list = []
for i in emojis_list:
    new_list.append(emoji.emojize(i))
print(new_list)         
sentence = input()
print("Hi there!")

def ask_for_emoji():
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
            main(TERM, g.address)
        else: 
            main(TERM, LOCATION)       
    else:
        print("Sorry, I only accept emojis" + ' ' + emoji.emojize(':crying_face:'))
        ask_for_emoji()

ask_for_emoji()


'''emoji chart 
https://unicode.org/emoji/charts/full-emoji-list.html '''

'''import geocoder
g = geocoder.ip('me')
print(g.latlng)'''