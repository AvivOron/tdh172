#this is a a simple script for crawling
import bs4 as bs
import urllib.request

sauce = urllib.request.urlopen('http://benyehuda.org').read()
soup = bs.BeautifulSoup(sauce, "lxml")
allPs = soup.find_all('p')
for paragraph in allPs:
    print(paragraph.text)
