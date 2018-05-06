import random
from random import choices 
import emoji 
from emoji.unicode_codes import UNICODE_EMOJI

MAIN_QS = ["What do you fancy today?", "What food are you feeling?"]
emojis_list = [":pizza:",":ice_cream:", ":sushi:", ":spaghetti:", ":french_fries:", ":Vietnam:", ":United_States:", ":Italy:",  ":Spain:", ":China:"]
new_list = []
for i in emojis_list:
    new_list.append(emoji.emojize(i))
print(new_list)         
sentence = input()
print("Hi there!")
sentence = input(random.choice(MAIN_QS) + str(random.sample(new_list, 3)))
    
        
emoji_input = str(sentence)

#gets unicode of emoji
unicode = 'U+{:X}'.format(ord(emoji_input))

#gets text of emoji
text = UNICODE_EMOJI[emoji_input]

#saves text without colons
text_without_col = text[1:len(text)-1]
print(text_without_col)



