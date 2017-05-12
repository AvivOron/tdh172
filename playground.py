#this is a a simple script for crawling

#importing libs
import bs4 as bs
import urllib.request
import sys
import re
import linecache
import os
import unicodedata


#print (len(unicodedata.normalize('NFC','שּ')))

specialChars = {'/':' ','"':'\'','\\':' ','.':' ','*':' ','?':' ',':':' ',\
    '\r\n':' ','\n':' ','\r':' ','\t':' '}

def cleanSpecialCharsFromString(str):
	strArr = list(str)
	i=0
	while i<len(strArr): 
		if strArr[i] in specialChars:
			strArr[i] = specialChars[strArr[i]]
		i+=1
	str = ''.join(strArr)
	return str

#print (cleanSpecialCharsFromString("aviv.oron\\ how u doin? im good! \n \t *** :)"))
reversedDict = {'⠁':'א','⠃':'ב','⠛':'ג','⠙':'ד','⠓':'ה','⠺':'ו','⠵':'ז',\
    '⠭':'ח','⠞':'ט','⠚':'י','⠅':'כ','⠇':'ל','⠍':'מ','⠝':'נ',\
    '⠎':'ס','⠫':'ע','⠏':'פ','⠮':'צ','⠟':'ק','⠗':'ר','⠩':'ש','⠹':'ת',\
    ' ':' ','\r':'\r','\n':'\n'}


hebStr = "⠟⠚⠇⠁⠚⠃ ⠝⠍⠭⠝ ⠍⠚⠚⠭  ⠗⠺⠏⠮⠓ ⠇⠁\n" \
"⠝⠁⠅ ⠮⠭⠇ ⠝⠁⠅⠗⠃ ⠚⠞⠺⠍ ⠹⠁⠚⠗⠟⠃ ⠗⠚⠩⠇ ⠓⠝⠵⠁⠓⠇\n" \
"\n" \
"⠹⠙⠍⠭⠝ ⠓⠗⠏⠮ ⠅⠃⠺⠩ ⠃⠗ ⠍⠺⠇⠩\n" \
"  ⠚⠝⠺⠇⠭ ⠇⠁ ⠍⠭⠓ ⠹⠺⠮⠗⠁⠍\n" \
"⠓⠹⠇⠅ ⠚⠩⠏⠝ ⠓⠍ ⠃⠗⠫ ⠚⠅ ⠅⠇⠺⠟ ⠇⠁\n" \
"⠚⠝⠺⠫⠍ ⠅⠃⠵⠫⠃ ⠏⠗⠭⠃\n" \
 "\n" \
"⠓⠗⠟⠚⠓ ⠚⠗⠺⠏⠮ ⠚⠗⠏⠎ ⠚⠗⠍⠵\n" \
"⠹⠺⠁⠇⠏⠝ ⠍⠚⠟⠭⠗⠍ ⠮⠗⠁⠍\n" \
"⠓⠏⠚⠓ ⠓⠍⠭⠓ ⠮⠗⠁⠃ ⠍⠩ ⠍⠛⠓\n" \
"⠹⠺⠁⠇⠹⠓ ⠹⠺⠫⠗⠓ ⠓⠝⠚⠃⠗⠹\n" \
 

hebStr = hebStr.split('\n')
translatedString = ""
for line in hebStr:
	string = list(line)
	braileList = []
	i = 0
	for char in string:
		charToAdd = reversedDict[char]
		if 0 <= i-1 and ord(string[i-1]) == 32:
			if charToAdd == 'כ':
				charToAdd = 'ך'
			elif charToAdd == 'מ':
				charToAdd = 'ם'
			elif charToAdd == 'נ':
				charToAdd = 'ן'
			elif charToAdd == 'צ':
				charToAdd = 'ץ'
			elif charToAdd == 'פ':
				charToAdd = 'ף'

		braileList = [charToAdd] + braileList #inserts word in the right order (append insert it in the wrong order)
		i+=1
	translatedString += ''.join(braileList) + "\n"

path = "res.txt"
with open(path, "w",encoding='utf-8') as songFile:
    songFile.write(translatedString)