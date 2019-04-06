# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 19:10:40 2019

@author: drose
"""

import requests
import xmltodict #makes XML feel like working with JSON, parsers it to dict
import json
import re
import math
from textblob import TextBlob as tb #using this for TF-IDF
#It provides a simple API for diving into common (NLP) tasks


r = requests.get("""http://feeds.feedburner.com/TechCrunch/""") #gets webpage
new_r = r.text #new is the read version as is of the webpage
parser_r =json.loads(json.dumps(xmltodict.parse(new_r))) 
#parsering the xml format of webpage, creating dict
parser_data  = parser_r['rss']['channel']['item'] 
#a list of dicts, containing the info
all_articles=[] #a list of lists of all info asked for about each article
list_of_data = [] #data of each article

blacklist = ['a','about','after','all','also','an','and','any','as','at','back','be','because','but','by','can','come','could','day','do','even','first','for','from','get','give','go','good','have','he','her','him','his','how','I','if','in','into','it','its','just','know','like','look','make','me','most','my','new','no','not','now','of','on','one','only','or','other','our','out','over','people','say','see','she','so','some','take','than','that','the','their','them','then','there','these','they','think','this','time','to','two','up','us','use','want','way','we','well','what','when','which','who','will','with','work','would','year','you','your' ]
#blacklist is 100 most common words in english    

WORDLIST_FILENAME = "words.txt" 
"""
I looked for a package that does this automatically, such as enchant or nltk,
but had problems with installing them. this list contains 55900 english words so i assume 
it should be good enough
"""
inFile = open(WORDLIST_FILENAME, 'r')
line = inFile.readline()
wordlist = line.split() #turning wordlist flie into a list of words 
    
def tf(word, blob): #number of times a word appears in a document blob, normalized by dividing by the total number of words in blob
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist): #number of documents containing word
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist): 
    #inverse document frequency, the more common a word is, the lower its idf
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))
    #ratio of the total number of documents to the number of documents containing word, 
    #then take the log of that and add 1 to the divisor to prevent division by zero.

def tfidf(word, blob, bloblist): 
    # computes the TF-IDF score. It's the product of tf and idf.
    return tf(word, blob) * idf(word, bloblist)


for dic in parser_data: 
   """
   goes over every dict, adds to list the title, the link and tag words
   and bold words if exsist, and creates a list of list of info, and a list of all "data"
   which is the atricle itself
   """
   val =[] #for each article
   val.append(dic['title']) 
   val.append(dic['link'])
   val.extend(dic['category'])
   data = (dic['content:encoded'])
   bold = re.findall(r'<b>(.*?)\<b>', data) #all the words in bold if exist
   val.extend(bold)
   
   list_of_data.append(tb(str(data)))
   all_articles.extend([val])
   

for i, blob in enumerate(list_of_data):
    """
    For each article, store the TF-IDF scores in a dictionary scores 
    mapping word score using a dict comprehension.
    then for each article take 10 most common words, gets rid of words that are not actual 
    words(just a scrumble of letters or non letters), 
    gets rid of basic english structure words (the, a, then...)
    makes sure word wasn't't already used as a tag (inserted manually)
    and if so, adds it to important words list
    """
    tfidf_words=[]
    scores = {word: tfidf(word, blob, list_of_data) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:10]:
        if word.isalpha() is True: #making sure only words made out of letters come back   
            word = word.lower()
            if word in wordlist: #making sure its an actual word
                if word not in blacklist: #making sure its an intresting word
                    existing_tags = all_articles[i][3:] 
                    if word.lower() not in existing_tags and word.upper() not in existing_tags and word.capitalize() not in existing_tags:
                        #making sure word isnat already there due to manully tagging (val.extend(dic['category']))
                        tfidf_words.append(word)
    all_articles[i].extend(tfidf_words)

"""
just priniting nicely, easy to understand and debug
"""
for i in all_articles:
   print("Name:")
   print(i[0])
   print("Link to article:")
   print(i[1])
   print("important words:")
   print (i[3:])
   print("\n")

#print(all_articles)

