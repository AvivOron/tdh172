import sys
import os
import wikipedia
import re
import MySQLdb
import csv


myDB = MySQLdb.connect(host="tdh.cmq2zbutzn8e.us-west-2.rds.amazonaws.com",port=3306,user="bialik",passwd="12345678",db="tdh172",charset='utf8')
cHandler = myDB.cursor()
wikipedia.set_lang("he")
cHandler.execute("SELECT id,name,wikipedia_name from poets")
poets = cHandler.fetchall()
#try:
for poet in poets:
	poet_id = poet[0]
	poet_name = poet[1]
	wikipedia_name = poet[2]
	
	csv_file = csv.reader(open('lexicon-csv.csv', "rt", encoding="utf8"), delimiter=",")
	for row in csv_file:
		if poet_name == row[1]:
			year_of_birth = row[2]
			year_of_death = row[3]
			viaf_id = row[4]

	if(wikipedia_name):
		page = wikipedia.page(wikipedia_name.replace("\"",""))
		if(page):
			summary = page.summary

	if(not summary):
		summary = ""

	input = [year_of_birth,year_of_death,viaf_id,summary, poet_id]
	cHandler.execute("UPDATE poets set year_of_birth=%s,year_of_death=%s,viaf_id=%s, summary=%s where id=%s;", input)
	myDB.commit()
	summary = ""
#except:
#print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

myDB.close()
