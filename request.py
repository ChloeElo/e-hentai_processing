import requests
import pickle
import time

with open('idtokens.p','rb') as file: idtokens = pickle.load(file)

if False:
    galleries = {}
else:
    with open('metadata.p','rb') as file: galleries = pickle.load(file)

finalnum = len(idtokens)
num = 0
while True:
    print('Current num', num)
    
    payload = {
        "method": "gdata",
        "gidlist": [],
        "namespace": 1
    }
    
    if num+25<finalnum: sublist = idtokens[num:num+25]
    else: sublist = idtokens[num:finalnum]
    
    payload['gidlist'] = sublist
    
    r = requests.post(r'https://api.e-hentai.org/api.php',json=payload)
    
    if r.status_code != 200:
        print('Request failed on num',num,'with code',r.status_code)
        with open('metadata.p','wb') as file: pickle.dump(galleries,file)
        raise SystemExit
    
    data = r.json()['gmetadata']
    
    for g in data: galleries[g['gid']] = g
    
    num+=25
    
    if num>finalnum: break
    
    time.sleep(1)
    
with open('metadata.p','wb') as file: pickle.dump(galleries,file) 