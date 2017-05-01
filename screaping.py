#this is a a simple script for crawling

#importing libs
import bs4 as bs
import urllib.request
import sys

#opening url, making soup with bs4
sauce = urllib.request.urlopen('http://benyehuda.org/bialik/').read()
soup = bs.BeautifulSoup(sauce, "lxml")

#find requested song
a = soup.find("a",text = "אל הצפור")


#creating inner link for the song
newlink = 'http://benyehuda.org/bialik/' + a['href']

#TEST:
#print(newlink)

#opening song url and making soup
sauce = urllib.request.urlopen(newlink).read()
soup = bs.BeautifulSoup(sauce, "lxml")
#find lines of the song
ps = soup.find_all(attrs={"class":"a3"})
dict = {'א':"⠁"}

#cleaning NIKUD!
i=0
for p in ps:
    string = list(p.text)
    while i<len(string):
        if not(ord(string[i])>=1488 and ord(string[i])<=1514 or string[i]==' ' ):
            del(string[i])
        i+=1

#writing into file
i=0
with open("text.txt", "w") as f:
        f.write(str(ord(dict['א'])))
