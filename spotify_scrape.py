import requests
import os
import string

# variables
CWD = os.getcwd()
LOCATION = os.path.join(CWD,'MUSIC')
if os.path.isdir(LOCATION)==False:
    os.mkdir(LOCATION)


def get_ID(session, id):
    import pdb;pdb.set_trace()
    LINK = f'https://api.spotifydown.com/getId/{id}'
    headers = {
        'authority': 'api.spotifydown.com',
        'method': 'GET',
        'path': f'/getId/{id}',
        'origin': 'https://spotifydown.com',
        'referer': 'https://spotifydown.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-fetch-mode': 'cors',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    response = session.get(url=LINK, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    return None


def generate_Analyze_id(session, yt_id):
    import pdb;pdb.set_trace()
    DL = 'https://corsproxy.io/?https://www.y2mate.com/mates/analyzeV2/ajax'
    data = {
        'k_query': f'https://www.youtube.com/watch?v={yt_id}',
        'k_page': 'home',
        'hl': 'en',
        'q_auto': 0,
    }
    headers = {
        'authority': 'corsproxy.io',
        'method': 'POST',
        'path': '/?https://www.y2mate.com/mates/analyzeV2/ajax',
        'origin': 'https://spotifydown.com',
        'referer': 'https://spotifydown.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-fetch-mode': 'cors',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    RES = session.post(url=DL, data=data, headers=headers)
    if RES.status_code == 200:
        return RES.json()
    return None


def generate_Conversion_id(session, analyze_yt_id, analyze_id):
    DL = 'https://corsproxy.io/?https://www.y2mate.com/mates/convertV2/index'
    data = {
        'vid': analyze_yt_id,
        'k': analyze_id,
    }
    headers = {
        'authority': 'corsproxy.io',
        'method': 'POST',
        'path': '/?https://www.y2mate.com/mates/analyzeV2/ajax',
        'origin': 'https://spotifydown.com',
        'referer': 'https://spotifydown.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-fetch-mode': 'cors',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    RES = session.post(url=DL, data=data, headers=headers)
    if RES.status_code == 200:
        return RES.json()
    return None


def returnSPOT_ID(link):
    return link.split('/')[-1].split('?si')[0]
SPOTIFY_PLAYLIST_LINK = input('Spotify Link : ')
OFFSET_VARIABLE = 0 #<-- Change to start from x number of songs

ID = returnSPOT_ID(SPOTIFY_PLAYLIST_LINK)
print('[*] SPOTIFY PLAYLIST ID    : ',ID)

headers = {
        'authority': 'api.spotifydown.com',
        'method': 'GET',
        'path': f'/trackList/playlist/{ID}',
        'scheme': 'https',
        'accept': '*/*',
        'dnt': '1',
        'origin': 'https://spotifydown.com',
        'referer': 'https://spotifydown.com/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
Playlist_Link = f'https://api.spotifydown.com/trackList/playlist/{ID}'

session = requests.Session()

offset_data = {}

offset = OFFSET_VARIABLE
page = 0
offset_data['offset'] = offset

response = session.get(url = Playlist_Link,headers=headers,params=offset_data )

while offset != None :
    if response.status_code == 200 :
        Tdata = response.json()['trackList']
        page = response.json()['nextOffset']
        for count,song in enumerate(Tdata):
            yt_id = get_ID(session=session, id=song['id'])
            if yt_id is not None:
                filename = song['title'].translate(str.maketrans('', '', string.punctuation)) + ' - ' + song['artists'].translate(str.maketrans('', '', string.punctuation)) + '.mp3'
                print('*'*25, str(count+1) + '/' + str(len(Tdata)), '*'*25)
                print('[*] Name of Song         : ', song['title'])
                print('[*] Spotify ID of Song   : ',song['id'])
                print('[*] Youtube ID of Song   : ',yt_id['id'])
                try:
                    data  = generate_Analyze_id(session = session, yt_id = yt_id['id'])
                    DL_ID = data['links']['mp3']['mp3128']['k']
                    DL_DATA = generate_Conversion_id(session= session,  analyze_yt_id = data['vid'], analyze_id = DL_ID )
                    DL_LINK = DL_DATA['dlink']
                    ## DOWNLOAD
                    link= session.get(DL_LINK)
                    ## Save
                    with open(os.path.join(LOCATION, filename), 'wb') as f:
                        f.write(link.content)
                except Exception as error_status:
                    print('[*] Error Status Code : ',error_status)
            else:
                print('[*] No data found for : ', song)
    if page!=None:
        offset_data['offset'] = page
        response = session.get(url = Playlist_Link, params=offset_data, headers=headers)
    else:
        break

