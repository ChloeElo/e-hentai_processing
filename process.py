from bs4 import BeautifulSoup

galleries = {}

for i in range(1,53):

    htmlfile = fr"C:\Users\SysAdmin\Pictures\AIprolif\{i}.html"

    with open(htmlfile,'r', encoding="utf8") as file: text = file.read()

    html = BeautifulSoup(text,'html.parser')

    #print(html.prettify())
    table = html.find("table",class_="gltm")
    links = table.find_all("a")

    for i in range(len(links)):
        link = links[i]['href']
        
        if not '/g/' in link: continue
        numbers = link.split('/g/')[-1]
        id, token = numbers.split('/')[:2]
        galleries[int(id)] = token

print(len(galleries))

idtokens = [ [id,token] for id,token in galleries.items() ]

idtokens.sort()
    
print(len(idtokens))

import pickle

with open('idtokens.p','wb') as file: pickle.dump(idtokens,file)

