import sys
import os
import MySQLdb
import codecs
import unicodedata
import dicttoxml
import collections

#sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print('hello, Yul')


myDB = MySQLdb.connect(host="tdh.cmq2zbutzn8e.us-west-2.rds.amazonaws.com",port=3306,user="bialik",passwd="12345678",db="tdh172",charset='utf8')
cHandler = myDB.cursor()
cHandler.execute("SELECT poems.name,original_data,wikipedia_name,poems.id, year_of_birth, year_of_death from poems JOIN poets ON poet_id = poets.id LIMIT 3")
poems_data = cHandler.fetchall()

for poem in poems_data:
	poem_name = poem[0]
	poem_data = poem[1]
	poet_name = poem[2]
	poem_id = poem[3]
	year_of_birth = poem[4]
	year_of_death = poem[5]
	poet_years = str(year_of_birth) +" - " + str(year_of_death)

	json_data = {
		'text': {
	   	'body': {
	   	'div1': ['type="poem" xml:id="d3"']
		   	}
		}
	}

	raw_paragraphs = poem_data.split('\xa0')
	paragraphs = []
	for p in raw_paragraphs:
		paragraphs.append(line for line in p.split('\n') if line)

	poem_dict = collections.OrderedDict()
	poem_dict['head'] = poem_name
	poem_dict['docAuthor'] = poet_name
	poem_dict['docDate'] = poet_years
	poem_dict['paragraphs'] = paragraphs

	json_data['text']['body']['div1'] = poem_dict

	def item_func(x):
		if x == "paragraphs":
			return "lg"
		else:
			return "l"


	tei_file = dicttoxml.dicttoxml(json_data, attr_type=False, item_func=item_func).decode('utf8')
	tei_file = tei_file.replace('<lg >', '<lg type="stanza">')
	tei_file = tei_file.replace('<body>', '<body xml:id="d2">')
	tei_file = tei_file.replace('<text>', '<text xml:id="d1">')
	tei_file = tei_file.replace('<div1>', '<div1 type="poem" xml:id="d3">')
	tei_file = tei_file.replace('<paragraphs>', '')
	tei_file = tei_file.replace('</paragraphs>', '')



	# cHandler.execute("UPDATE poems set tei=tei_file where id=poem_id;")
	# myDB.commit()
	with open(r"C:\temp\example2.tei", "w", encoding='utf-8') as f:
		f.write(tei_file)
	
	#print(cleanNikudFromString(cleanSpecialCharsFromString(poem[1])))

myDB.close()