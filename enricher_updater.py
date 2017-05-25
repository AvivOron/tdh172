import sys
import os
import wikipedia
import re
import MySQLdb
import csv


myDB = MySQLdb.connect(host="tdh.cmq2zbutzn8e.us-west-2.rds.amazonaws.com",port=3306,user="bialik",passwd="12345678",db="tdh172",charset='utf8')
cHandler = myDB.cursor()
wikipedia.set_lang("he")
cHandler.execute("SELECT id,name from poets")
poets = cHandler.fetchall()
#try:
for poet in poets:
	poet_id = poet[0]
	poet_name = poet[1]
	#wikipedia_name = poet[2]
	gender = ""
	occupation = ""
	citizenship = ""
	place_of_birth = ""
	place_of_death = ""
	wikidata_id = 0

	csv_file = csv.reader(open('lexicon-csv.csv', "rt", encoding="utf8"), delimiter=",")
	for row in csv_file:
		if poet_name == row[0]:
			gender = row[2]
			occupation = row[4]
			citizenship = row[3]
			place_of_birth = row[7]
			place_of_death = row[8]
			wikidata_id = row[10]

	"""if(wikipedia_name):
		page = wikipedia.page(wikipedia_name.replace("\"",""))
		if(page):
			summary = page.summary

	if(not summary):
		summary = """""

	input = [gender,occupation,citizenship,place_of_birth,place_of_death,wikidata_id, poet_id]
	#print(input)
	cHandler.execute("UPDATE poets set gender=%s,occupation=%s,citizenship=%s, place_of_birth=%s, place_of_death=%s, wikidata_id=%s where id=%s;", input)
	myDB.commit()
	#summary = ""
#except:
#print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

myDB.close()
