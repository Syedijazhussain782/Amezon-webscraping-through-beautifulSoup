import requests
from bs4 import BeautifulSoup
import re
from fastapi import FastAPI
import uvicorn
app = FastAPI()



def tiktok(username):
    
    url = "https://www.tiktok.com/@"+username+"?lang=en"
    payload = {}
    headers = {
    'Cookie': 'msToken=dBKdPAmoyEWKDq04XP-czC6AcPIIK1sH8OQ4ksLThqB-D-5cmT8hXyMZxf-KIClx9ZwER8aTGJHNCJyZa3fKQyHZJQ6LsPCmHgBKWyYbtPagKPTSbhkRjgf9WM74smJzoXjMlUHcgDg=; tt_chain_token=QcfKnIB4BkT2lGqgj2d9rA==; tt_csrf_token=svBlPPwX-Qde_h3VmJWm7agtBrqQ4dqRx-88; ttwid=1%7C3AI8ZvzOdMnG59L3BWX0SrqFo3V1BTn_xUQjffq7c7g%7C1688452110%7C2f219e8c8ce7d6620ee2d1821f9974f3d8c3c4404959df9ab28097ddce7633e6'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
   
    soup = BeautifulSoup(response.text, 'html.parser')

    #USER_TITLE_NAME
    try:
        user_title = soup.find('h1', class_='e1457k4r8').text
        
    except:
        pass
    
    #USER_PROFILE_NAME
    try:
        profile_name = soup.find('h2', class_='ekmpd5l7').text
       
    except:
        pass
    
    #USER_PROFILE_PICTURE_URL
    try:
        profile_picture = soup.find('img', class_='e1e9er4e1')['src']
    except:
    
        pass
    #USER_DISCRIPTION
    try:
        user_discription = soup.find('h2', class_='e1457k4r3').text.replace('\n', '')
    except:
        pass
   
    #USER_FOLLOWINGS_FOLLOWERS_LIKES_COUNT
    try:
        
        txt = soup.find('h3').text

        txt_all_list = txt.split("Following")
        followings_count =txt_all_list[0]
       
        followers_count= txt_all_list[1].split("Followers")[0]
       
        followers = txt_all_list[1].split("Followers")
        likes_count  = followers[1].replace("Likes","")
     
        
        
    except:
        pass

    #USER_THUMBNAILS_UPTO_10
    try:
        thumbnails = []
        all = soup.find_all("div", {"class": "e1yey0rl0"})
        for tag in all[:10]:
            thumbnails.append(tag.find("img")['src'])
    except:
        pass

    data = {
        "Title_Name": user_title,
        "Name": profile_name,
        "Profile Picture": profile_picture,
        "user_discription":user_discription,
        "Following": followings_count,
        "Followers": followers_count,
        "Likes": likes_count,
        "Thumbnails": thumbnails,
    }
        
        
    return data
        
        
    

 
  
username = "poetrylines_01"
@app.get('/userdata/{username}')
def get_tiktokbasicdata(username):
    tiktoks=tiktok(username)
    
    return tiktoks


  
if __name__ == "__main__":
    # Use this for debugging purposes only
    
    uvicorn.run(app,host="0.0.0.0", port=8000, log_level="debug") 
  
  
  