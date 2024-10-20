import json
import requests as req
import pandas as pd
config = json.load(open('config.json'))

hdr = {
    'X-MAL-CLIENT-ID' : config['clientId']
    }

synop = []
animes = []
ranks = ['all', 'airing', 'tv', 'ova', 'movie', 'special', 'bypopularity', 'favorite']
for rank in ranks:
    with req.get('https://api.myanimelist.net/v2/anime/ranking?ranking_type='+ rank +'&limit=350', headers=hdr) as r:
            for node in json.loads(r.text)['data']:
                if not any(anime['id'] == node['node']['id'] for anime in animes):
                    animes.append({"id":node['node']['id'], "title":node['node']['title']})

r = ''

for anime in animes:
     with req.get('https://api.myanimelist.net/v2/anime/'+ str(anime['id']) +'?fields=id,title,synopsis', headers=hdr) as r:
        try:
             anime['synop'] = json.loads(r.text)['synopsis']
        except:
             anime['synop'] = 'deu ruim'

animes = [anime for anime in animes if anime['synop'] != 'deu ruim']
df = pd.DataFrame(animes)
df.to_csv('animeDataSet.csv')

print('Encerrado.')


