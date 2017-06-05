
#importing libs
import bs4 as bs
import urllib.request
import sys
import re
import linecache
import os
import unicodedata
import MySQLdb


dict = {'א':'⠁','ב':'⠃','ג':'⠛','ד':'⠙','ה':'⠓','ו':'⠺','ז':'⠵',\
    'ח':'⠭','ט':'⠞','י':'⠚','כ':'⠅','ך':'⠅','ל':'⠇','מ':'⠍','נ':'⠝',\
    'ס':'⠎','ע':'⠫','פ':'⠏','ף':'⠏','צ':'⠮','ץ':'⠮','ק':'⠟','ר':'⠗','ש':'⠩','ת':'⠹',\
    ' ':' ','-':' ','\r':'\r','ם':'⠍','ן':'⠝','\n':'\n'}

specialChars = {'/':' ','"':'\'','\\':' ','.':' ','*':' ','?':' ',':':' ',\
    '\r\n':' ','\n':' ','\r':' ','\t':' '}

sentencedToRemove = ['להאזנה לשיר','להאזנה  לשיר,' ,	'לדף הראשי', 'לתוכן  הענינים', 'לתוכן הענינים', 'לתוכן הענינים' , '©', 'כל הזכויות']

def ifSentenceToRemoveAppears(str):
	for s in sentencedToRemove:
		if(s in str):
			return 1
	return 0

def cleanNikudFromString(str):
	str = str.replace(u'\xa0', u' ')
	str = str.replace(u'\x0d', u' ')
	str = str.replace(u'\x0d', u' ') #problematic chars that look like space but are not
	strArr = list(str)

	i=0
	while i<len(strArr): # check which chars we want to remove and which not: "? /? and hebrew chars like וֹ, סּ (אותיות מנוקדות)
		decomposedUnicodeChar = unicodedata.normalize('NFC',strArr[i])
		if(len(decomposedUnicodeChar) > 1):
			strArr[i] = decomposedUnicodeChar[0]

		if not(ord(strArr[i])>=1488 and ord(strArr[i])<=1514 or strArr[i] == ' ' or strArr[i]== '-'): #newlines symbols and dash
			del(strArr[i])
			i-=1
		i+=1

	str1 = ''.join(strArr)
	return str1

def cleanSpecialCharsFromString(str):
	strArr = list(str)
	i=0
	while i<len(strArr): 
		if strArr[i] in specialChars:
			strArr[i] = specialChars[strArr[i]]
		i+=1
	str = ''.join(strArr)
	return str

#opening url, making soup with bs4 - (poet should be received from user)
sauce = urllib.request.urlopen('http://benyehuda.org/').read()
soup = bs.BeautifulSoup(sauce, "lxml")

myDB = MySQLdb.connect(host="tdh.cmq2zbutzn8e.us-west-2.rds.amazonaws.com",port=3306,user="bialik",passwd="12345678",db="tdh172",charset='utf8')
cHandler = myDB.cursor()

pattern = re.compile(r'כל השירה') #poetry section only
poetry = soup.find(text=pattern)
poetryCellInTable = poetry.parent.parent.parent #go to poetry html object
artistsLinks = poetryCellInTable.find_all("a")

for artistLink in artistsLinks:
	try:
		englishName = artistLink['href'].split('/')[0]
		link = 'http://benyehuda.org/' + artistLink['href']
		name = str(artistLink.contents[0])
		nameArr = str(artistLink.contents[0]).split('\n')
		parsedName = ''

		for l in nameArr:
			l = l.replace('\n', '').strip()
			if(len(l) > 0):
				parsedName = parsedName + ' ' + l
		parsedName = parsedName.strip()

		
		cHandler.execute("SELECT id from poets where name=%s; ", [parsedName])
		poetID = cHandler.fetchall()[0][0]
		print(poetID)
		if(poetID < 78):
			continue

		sauce = urllib.request.urlopen(link).read()
		soup = bs.BeautifulSoup(sauce, "lxml")
		songs = soup.find_all("a")
		regexp = re.compile(r'html')
		formattedArtistName = cleanNikudFromString(cleanSpecialCharsFromString(parsedName))[0:100]
		for song in songs:
			try:
				if regexp.search(str(song)):
					songName = str(song.text)
					songLink = str(song['href'])
					formattedSongName = cleanNikudFromString(cleanSpecialCharsFromString(songName))[0:100]
					sauce1 = urllib.request.urlopen(link + songLink).read()
					soup1 = bs.BeautifulSoup(sauce1, "lxml")
					ps = soup1.findAll(True, {'class':['a','a1','a2','a3','a4','a5','a6','a7','a8','a9','MsoNormal']})

					translatedString = ""
					originalString = ""
					for p in ps:
						try:
							noNikudStr = cleanNikudFromString(p.text)
							if(ifSentenceToRemoveAppears(noNikudStr)): #remove sentences like "לחזרה לדף הראשי\תוכן עניינים"
								continue

							string = list(noNikudStr)
							#making new list with Braille chars.
							braileList = []
							for char in string:
								braileList.append(dict[char]) #inserts word in the right order (append insert it in the wrong order)
							translatedString += ''.join(braileList) + "\n"
							originalString += cleanSpecialCharsFromString(p.text) + "\n"
						except:
							pass

					if(len(translatedString.split('\n')) > 5 and len(originalString) < 5000): #sanity
						path = str(formattedArtistName + "/" + formattedSongName + ".txt")
						os.makedirs(os.path.dirname(path), exist_ok=True)
						with open(path, "w",encoding='utf-8') as songFile:
						    songFile.write(translatedString)

						try:
							input = [formattedSongName, originalString, translatedString, poetID]
							cHandler.execute('''INSERT INTO poems ( name, original_data, translated_data, poet_id ) VALUES ( %s, %s, %s, %s); ''', input)
							myDB.commit()
							print("done" + formattedSongName)
						except:
							myDB.rollback()
							print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
							break

			except Exception as e: 
					print ("couldnt open " + songName + " " + str(e))
					print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
					pass
		


	except Exception as e: 
		print ("couldnt open " + str(englishName) + " " + str(e))
		print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
		pass
		

myDB.close()