# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 19:10:40 2019

@author: drose
"""

import requests
import xmltodict #makes XML feel like working with JSON, parsers it to dict
import json

r = requests.get("""http://feeds.feedburner.com/TechCrunch/""") #gets webpage
new_r = r.text #new is the read version as is of the webpage
parser_r =json.loads(json.dumps(xmltodict.parse(new_r))) #parsering the xml format of webpage, creating dict
parser_data  = parser_r['rss']['channel']['item'] #a list of dicts, containing the info


for dic in parser_data: #goes over every dict, adds to list the title, the link and important words, prints list and memset it for next one
   val =[]
   val.append(dic['title']) 
   val.append(dic['link'])
   val.extend(dic['category'])

   print(val)
   val = []
    




