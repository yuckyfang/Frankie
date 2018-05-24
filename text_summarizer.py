from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

#sample text 
text = '''Data science is an interdisciplinary field of scientific methods, processes, algorithms and systems to extract knowledge 
or insights from data in various forms, either structured or unstructured, similar to data mining.
Data science is a "concept to unify statistics, data analysis, machine learning and their related methods" in order to
"understand and analyze actual phenomena" with data.It employs techniques and theories drawn from many fields within 
the broad areas of mathematics, statistics, information science, and computer science.
Turing award winner Jim Gray imagined data science as a "fourth paradigm" of science (empirical, theoretical, computational 
and now data-driven) and asserted that "everything about science is changing because of the impact of information technology" 
and the data deluge. When Harvard Business Review called it "The Sexiest Job of the 21st Century" the term became 
a buzzword, and is now often applied to business analytics,business intelligence, predictive modeling, any arbitrary use 
of data, or used as a sexed-up term for statistics. In many cases, earlier approaches and solutions are now simply 
rebranded as "data science" to be more attractive, which can cause the term to "dilute beyond usefulness." While many 
university programs now offer a data science degree, there exists no consensus on a definition or curriculum contents.
Because of the current popularity of this term, there are many "advocacy efforts" surrounding it.'''
print(text)

#nltk.download('stopwords')
#nltk.download('punkt')

#stopwords do not add value to the meaning of a sentence eg the, a, of...
stopWords = set(stopwords.words("english")) #stores predefined stopwords from nltk 
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
#print('average ' + str(average))

#prints summary 
summary = ''
for sentence in sentences:
    if sentence in sentenceValue and sentenceValue[sentence] > (average): #prints sentence if above average 
        summary +=  " " + sentence
print(summary)