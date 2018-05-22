from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

#sample text 
text = '''Is pricing power gone? 2018 has been a perfect storm for Big Food. Sales growth is stalling while oil, freight  
raw material, steel and aluminum costs rise.  In the past, inflation wouldnt have been a major issue for these legacy brands. 
Their size, supply chain, and enormous TV advertising budgets allowed them to muscle out competitors and maintain higher prices.
You didnt have tons of competition, and the superior economics just continued, Brennan said. It was a pretty nice gig.
But they dont have that luxury anymore. Their business models and pricing power are crumbling as the retail and grocery 
industries consolidate, consumer allegiances fade, and low-budget digital advertising campaigns sway shoppers. 
Walmart (WMT), Amazon (AMZN), Target (TGT), and Kroger (KR) are waging a price war that has spread to the rest of the retail 
and grocery industry. The pricing battle has changed shoppers expectations of how much a box of cereal or a bar of soap costs.
If suppliers dont play ball on prices, Walmart can put products in the back of the store where shoppers cant find them. 
Amazon can send them to the bottom of its search pages. '''
print(text)

#nltk.download('stopwords')
#nltk.download('punkt')

#stopwords do not add value to the meaning of a sentence eg the, a, of...
stopWords = set(stopwords.words("english")) #store predefined stopwords from nltk 
words = word_tokenize(text) #separate every word in the text and store in array

#stores frequency of each word
freqTable = dict()
for word in words:
    word = word.lower()
    if word in stopWords: #skips stopword
        continue
    if word in freqTable:
        freqTable[word] += 1 #go through every word and record frequency 
    else:
        freqTable[word] = 1 #add word to table
        
sentences = sent_tokenize(text) #separates each sentence 
sentenceValue = dict() #stores value of each sentence based on frequency of each word through entire text 

for sentence in sentences:
     for index, wordValue in enumerate(freqTable, start=1):
          if wordValue in sentence.lower(): # index[0] return word
               if sentence in sentenceValue:  
                    sentenceValue[sentence] += index # index returns value of occurrence of that word
                    #print(sentenceValue)
               else:
                    sentenceValue[sentence] = index
#print(sentenceValue)
          
sumValues = 0
for sentence in sentenceValue:
    sumValues += sentenceValue[sentence] #sum of each every sentence value 
average = int(sumValues/ len(sentenceValue)) # Average value of a sentence from original text
print('average ' + str(average))

#prints summary 
summary = ''
for sentence in sentences:
    if sentence in sentenceValue and sentenceValue[sentence] > (1.5*average): #prints sentence if above average 
        summary +=  " " + sentence
print(summary)