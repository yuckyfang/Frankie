from __future__ import print_function

import random
from random import choices 
import emoji 
from emoji.unicode_codes import UNICODE_EMOJI
import geocoder
import argparse, json, pprint, requests, sys, urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode


SEARCH_LIMIT = 3

with open("config.json", "r") as f:
    data = json.load(f)
API_KEY = data['api_key']
API_HOST = data["API_HOST"]
REVIEWS_PATH = data["REVIEWS_PATH"]
SEARCH_PATH = data["SEARCH_PATH"]
BUSINESS_PATH = data["BUSINESS_PATH"]
    
    
def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    
    #need the following parameters (type dict) 
#     params = {'name':'MinuteClinic', 'address1':'241 West 57th St', 'city':'New York', 'state':'NY', 'country':'US'}
#     param_string = urllib.parse.urlencode(params)
#     res = requests.request("GET", url, headers=headers, params = url_params)
#     data = res.json()
#     print(data)
#     
#     b_id = data['businesses'][0]['id'] 
#     r_url = "/v3/businesses/" + b_id + "/reviews"    #review request URL creation based on business ID
#     reviews = requests.request("GET",r_url,headers=headers, params = url_params)
#     print(reviews.json())
#     
    response = requests.request('GET', url, headers=headers, params=url_params)   
    return response.json()

    
def search(api_key, term, latitude, longitude, location=None):
    #Query the Search API by a search term and location.
    if location is None:
        url_params = {
            'term': term.replace(' ', '+'),
            'latitude': latitude, 
            'longitude': longitude, 
            'limit': SEARCH_LIMIT
    
        }
    else:
        url_params = {
            'term': term.replace(' ', '+'),
            'location': location, 
            'limit': SEARCH_LIMIT
    
        }
    
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    #Query the Business API by a business ID.
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)


def get_review(api_key, business_id):
    review_path = BUSINESS_PATH + business_id + REVIEWS_PATH
    return request(API_HOST, review_path, api_key)


#Queries the API by the input values from the user.
def query_api(term,latitude, longitude, location=None):
    try: 
        if location is None:
            response = search(API_KEY, term, latitude, longitude)
        else:
            response = search(API_KEY, term, None, None, location)
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
        #prints name, phone, location, hours, and rating of each business 
        print('')
        print(response['name'])
        print(response['phone'])
        pprint.pprint(response['location']['display_address'])
        print(str(response['rating']) + ' stars')
        #prints 3 reviews of each business 
        review = get_review(API_KEY, businesses[0]['id'])
        pprint.pprint(review['reviews'][0]['rating'])
        pprint.pprint(review['reviews'][0]['text'])
        pprint.pprint(review['reviews'][1]['rating'])
        pprint.pprint(review['reviews'][1]['text'])
        pprint.pprint(review['reviews'][2]['rating'])
        pprint.pprint(review['reviews'][2]['text'])
        pprint.pprint(response['hours'])
        print('')
        print(response2['name'])
        print(response2['phone'])
        pprint.pprint(response2['location']['display_address'])
        print(str(response2['rating']) + ' stars')
        review2 = get_review(API_KEY, businesses[1]['id'])
        pprint.pprint(review2['reviews'][0]['rating'])
        pprint.pprint(review2['reviews'][0]['text'])
        pprint.pprint(review2['reviews'][1]['rating'])
        pprint.pprint(review2['reviews'][1]['text'])
        pprint.pprint(review2['reviews'][2]['rating'])
        pprint.pprint(review2['reviews'][2]['text'])
        pprint.pprint(response2['hours'])
        print('')
        print(response3['name'])
        print(response3['phone'])
        pprint.pprint(response3['location']['display_address'])
        print(str(response3['rating']) + ' stars')
        review3 = get_review(API_KEY, businesses[2]['id'])
        pprint.pprint(review3['reviews'][0]['rating'])
        pprint.pprint(review3['reviews'][0]['text'])
        pprint.pprint(review3['reviews'][1]['rating'])
        pprint.pprint(review3['reviews'][1]['text'])
        pprint.pprint(review3['reviews'][2]['rating'])
        pprint.pprint(review3['reviews'][2]['text'])
        pprint.pprint(response3['hours'])


#         pprint.pprint(response, indent=2)
#         print('')
#         pprint.pprint(response2, indent=2)
#         print('')
#         pprint.pprint(response3, indent=2)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
                )
            )
        
        
def get_location(term):
    LOCATION = input("location?")
    locations = ['near me', 'current location', 'here', 'around me', 'around here', 'current', 'me', 'right here']
    if LOCATION.lower() in locations: 
        g = geocoder.ip('me')
        query_api(term,g.latlng[0], g.latlng[1])
    else: 
        query_api(term, None, None, LOCATION)
        
          
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
        #saves text without colons aka search term
        TERM = text[1:len(text)-1]
        get_location(TERM)
             
    else:
        print("Sorry, I can only read emojis" + ' ' + emoji.emojize(':crying_face:'))
        ask_for_emoji()
    
ask_for_emoji()

