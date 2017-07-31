#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Pool, TimeoutError
import xml.etree.ElementTree
import collections
import os, sys
import requests
from bs4 import BeautifulSoup
import lxml
from _collections import defaultdict
from _random import Random
import random
import time
import MySQLdb
import codecs
import unicodedata

def find_places(text):
    ret=defaultdict(list)
    url='http://yeda.cs.technion.ac.il:8088/MWE/analysis.jsp'
    payload ={'input_text': text}
    print("step in")
    r= requests.post(url,timeout=50,data=payload)
    print("step out")
    content= r.content
    soup = BeautifulSoup(content, "xml")
    for sentence in soup.find_all('sentence'):
        sent=""
        for token in sentence:
            sent=sent+' '+token['surface']
            sent=sent.replace('.' ,'')
        for token in sentence.find_all('token'):
            for analysis in  token.find_all('analysis'):
                if analysis.has_attr('score'):
                    if analysis['score']=='1.0' :##or '0.5':
                        try:
                            type=analysis.find('base').find('properName')['type'] 
                            if type== 'town' or type == 'country' or type=='location':
                                ret[(analysis.find('base')['lexiconItem'])].append(sent) 
                                #print(analysis.find('base')['lexiconItem'])
                        except:
                            pass
                        try:
                            type=analysis.find('base').find('MWE')['type'] 
                            if type == 'town' or type == 'country' or type =='location':
                                #print(analysis.find('base').find('MWE')['multiWordUndotted'])
                                ret[(analysis.find('base').find('MWE')['multiWordUndotted'])].append(sent)
                        except:
                            pass
    return ret

def locate_places_by_bounds(place):
    url = 'https://maps.googleapis.com/maps/api/geocode/xml?address=' + place
    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.content, 'xml')
    try:
        geometry = soup.find('geometry')
        viewport = geometry.find('viewport')
        southwest = viewport.find('southwest')
        sw_lat = float(southwest.find('lat').text)
        sw_lng = float(southwest.find('lng').text)
        northeast = viewport.find('northeast')
        ne_lat = float(northeast.find('lat').text)
        ne_lng = float(northeast.find('lng').text)
        lat= random.uniform(sw_lat,ne_lat)
        lng =random.uniform(sw_lng,ne_lng)
    except:
        return (None,None)
    
    return  (lat,lng)
    



def locate_places(place):
    url = 'https://maps.googleapis.com/maps/api/geocode/xml?address=' + place
    r = requests.get(url, timeout=5)
    soup = BeautifulSoup(r.content, 'xml')
    try:
        geometry = soup.find('geometry')
        location = geometry.find('location')
        sw_lat = float(location.find('lat').text)
        sw_lng = float(location.find('lng').text)
        up_or_down=random.uniform(0.0,1.0)
        left_or_right=random.uniform(0.0,1.0)
        if(up_or_down>0.5):
            pass
        
        
        
    except:
        return (None,None)
    
    return  (lat,lng)




myDB = MySQLdb.connect(host="tdh.cmq2zbutzn8e.us-west-2.rds.amazonaws.com",port=3306,user="bialik",passwd="12345678",db="tdh172",charset='utf8')
cHandler = myDB.cursor()
cHandler.execute("SELECT poems.name,original_data,wikipedia_name,poems.id, year_of_birth, year_of_death from poems JOIN poets ON poet_id = poets.id")
poems_data = cHandler.fetchall()
mainDict = dict()
i = 0
for poem in poems_data:
	print(str(i))
	i = i+1
	poem_name = poem[0]
	poem_data = poem[1]
	poet_name = poem[2]
	poem_id = poem[3]
	year_of_birth = poem[4]
	year_of_death = poem[5]
	poet_years = str(year_of_birth) +" - " + str(year_of_death)

	string = poem_data
	while True:
		try:
			dic = find_places(string.replace('\n','.\n'))
		except Exception:
			print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
			time.sleep(5)
			continue
		break

	for place in dic.keys():
		if(not place in mainDict):
			mainDict[place] = 1;
		else:
			mainDict[place] += 1;

	#fName = """C:\\temp\\""" + str(poet_name) + """\\""" + str(poem_name) + """.txt"""
	#fName = fName.replace('"',"")
	#os.makedirs(os.path.dirname(fName), exist_ok=True)
	#with open(fName, "w", encoding='utf-8') as f:
	#	f.write(tei_file)

	
myDB.close()
fName = """C:\\temp\\res.txt"""
os.makedirs(os.path.dirname(fName), exist_ok=True)
with open(fName, "w", encoding='utf-8') as f:
	for place in mainDict.keys():
		f.write(place + "	" + str(mainDict[place]) + "	" + str(locate_places_by_bounds(place)) +"\n")