import os

path = '/home/gilad/Desktop/temp/'
newpath = '/home/gilad/Desktop/new/'
print (path)
i=0
for filename in os.listdir(path):

    F = open(path+filename,"r") 
   # print (F)
    N = open(newpath+filename,"w")
    text = F.read()
    data =text[text.find("<head>"):text.find("<lg")]
    
    title = "<title>"+text[text.find("<head>")+6:text.find("</head>")]+"</title>"

    poet = "<poet>"+text[text.find("<docAuthor>")+11:text.find("</docAuthor>")]+"</poet>"
    poetYears = "<poetYears>"+text[text.find("<docDate>")+9:text.find("</docDate>")]+"</poetYears>"
    print(poetYears)
    header="""<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <fileDesc>
    <titleStmt>"""+title+poet+poetYears+"""</titleStmt>
    <publicationStmt><date>2017</date></publicationStmt>
      <sourceDesc>
        <p>Ben Yehuda Project</p>
              <creator>
        Aviv Oron , Gilad Winterfeld
      </creator>
      </sourceDesc>

    </fileDesc>


  </teiHeader>  <text>
    <body>"""
    end="""    </body>
  </text>
</TEI>"""
    body = text[text.find("<lg"):text.find("</div1>")]
    print(i)
    # N.write(F.read())

    N.write(header+body+end)
    print (F.read())
    i=i+1

    # do your stuff
