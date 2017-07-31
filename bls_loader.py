import sys
import os
import MySQLdb

path = 'new/'
myDB = MySQLdb.connect(host="tdh.cmq2zbutzn8e.us-west-2.rds.amazonaws.com",port=3306,user="bialik",passwd="12345678",db="tdh172",charset='utf8')
cHandler = myDB.cursor()

for filename in os.listdir(path):
  with open(path+filename, "r", encoding='utf-8') as f:
    text = f.read()
    text = text.replace("<", "&lt;").replace(">","&gt;")
    poem_id = filename.replace(".xml","")
    input = [text, poem_id]
    cHandler.execute("UPDATE poems set tei=%s where id=%s;", input)
    myDB.commit()
    print(poem_id)
