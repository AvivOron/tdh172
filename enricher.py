import sys
import os
import wikipedia
import re
import MySQLdb

myDB = MySQLdb.connect(host="tdh.cmq2zbutzn8e.us-west-2.rds.amazonaws.com",port=3306,user="bialik",passwd="12345678",db="tdh172",charset='utf8')
cHandler = myDB.cursor()
wikipedia.set_lang("he")
cHandler.execute("SELECT id,name from poets")
poets = cHandler.fetchall()
for poet in poets:
	poet_id = poet[0]
	poet_name = poet[1]
	#print("poet: " + poet_name)
	cHandler.execute("SELECT name from poems where poet_id = " + str(poet_id))
	poems = cHandler.fetchall()
	pages = wikipedia.search(poet_name)
	ranks = []
	for i in range(len(pages)):
		ranks.append(0)

	i = 0
	for page in pages:
		try:
			pageObj = wikipedia.page(page)
			#setattr(pageObj, 'rank', 0)
			
			for poem in poems:
				poem_name = poem[0]
				#print("poem: " + poem_name)
				if(poem_name in pageObj.content):
					ranks[i] += 1
			i +=1
		except wikipedia.exceptions.DisambiguationError as e:
			pass
		except:
			i += 1
			print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
			pass

	i = 0
	maxRefers = 0
	index = 0
	for x in range(0, len(pages)):
		if(ranks[x] > maxRefers):
			maxRefers = ranks[x]
			index = x
	
	try:
		page = wikipedia.page(pages[index])

		year_of_birth = "";
		year_of_death = "";
		match1 = re.match(r'.*([1-3][0-9]{3})', page.links[0])
		match2 = re.match(r'.*([1-3][0-9]{3})', page.links[1])
		if match1 is not None and match2 is not None:
			year_of_birth = match1.group(1)
			year_of_death = match2.group(1)

		input = [page.title, page.url,year_of_birth,year_of_death, poet_id]
		#dont override existing data!! 
		#cHandler.execute("UPDATE poets set wikipedia_name=%s ,wikipedia_url=%s, year_of_birth=%s,year_of_death=%s where id=%s;", input)
		#myDB.commit()
	except:
		print("failed for " + str(poet_id))

myDB.close()
