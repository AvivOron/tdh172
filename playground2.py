import sys
import os
import wikipedia
import re
import MySQLdb

wikipedia.set_lang("he")
page = wikipedia.page("רחל המשוררת")
print(page.summary)
