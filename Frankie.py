import random
from random import choices 
import emoji 
from emoji.unicode_codes import UNICODE_EMOJI

MAIN_QS = ["What do you fancy today?", "What food are you feeling?"]
emojis_list = [":pizza:",":icecream:", ":curry:", ":sushi:", ":spaghetti:", ":fries:", ":us:", ":jp:", ":it:", ":uk:", ":es:"]
new_list = []
for i in emojis_list:
    new_list.append(emoji.emojize(i))
         
def greeting():
    sentence = input()
    return "Hi there!"

def extract_emoji():
    print(sentence = input(random.choice(MAIN_QS + random.sample(new_list, 3))))
    
        
    emoji_input = str(sentence)
    
    #gets unicode of emoji
    unicode = 'U+{:X}'.format(ord(emoji_input))
    
    #gets text of emoji
    text = UNICODE_EMOJI[emoji_input]

    #saves text without colons
    text_without_col = text[1:len(text)-1]
    return text_without_col

def main():    
    print(greeting())
    print(extract_emoji())
    
main()

'''next steps: take text_without_colon and use keyword to search yelp's categories, ask for location, then find best rated ones with
most positive reviews'''
#(emoji.emojize(":jp:"))
#s = '😀'

