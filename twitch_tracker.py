import requests
import json
import time

#GLOBAL
CLIENT_ID = ""
SECRET_ID = ""
CHANNEL_NAME = ""
WEBHOOK = ""

#FILLING GLOBAL VARS
with open("settings.json","r") as f:
    settings = json.load(f)
    CLIENT_ID = settings["CLIENT_ID"]
    SECRET_ID = settings["SECRET_ID"]
    CHANNEL_NAME = settings["CHANNEL_NAME"]
    WEBHOOK = settings["WEBHOOK"]

CHANNELS = {}
for channel in CHANNEL_NAME:
    CHANNELS[channel] = False

#OBTAINING APP TOKEN
APP_TOKEN = requests.post("https://id.twitch.tv/oauth2/token", data=f"client_secret={SECRET_ID}&client_id={CLIENT_ID}&grant_type=client_credentials").json()["access_token"]


headers = {"Content-Type": "application/json"}
embed = {
    "title": "",
    "description": "",
    "color": 16711680,  # Hexadecimal para el color rojo
    'thumbnail': {
        'url': "",
        "height": 400,
        "width": 400
    },
    "fields": [
        {
            "name": "",
            "value": "",
            "inline": False,
        }
    ],
    "footer": {
        "text": "Como dijo meritofeles mas vale respirar que no hacerlo"
    }
}

while True:
    for channel, live in CHANNELS.items():
        try:
            image_req = requests.get(f"https://api.twitch.tv/helix/users?login={channel}", headers={"Client-ID": CLIENT_ID, "Authorization": f"Bearer {APP_TOKEN}"}).json()
            response = requests.get(f"https://api.twitch.tv/helix/streams?user_login={channel}", headers={"Client-ID": CLIENT_ID, "Authorization": f"Bearer {APP_TOKEN}"}).json()
            
            is_live = len(response["data"]) > 0     #CHECKING IF LIVE

            #FILLING EMBED
            embed["thumbnail"]["url"] = image_req["data"][0]["profile_image_url"]
            embed["description"] = response["data"][0]["title"]
            embed["title"] = f"{channel} is now online"
            embed["fields"][0]["value"] = f"https://www.twitch.tv/{channel}"
            
            if is_live and live == False:
                CHANNELS[channel] = True
                live = requests.post(WEBHOOK, json={ "embeds": [embed] }, headers=headers)
                #print(f'El canal {channel} está en vivo')    
            elif is_live == False and live == True:
                CHANNELS[channel] = False
                #print(f'El canal {channel} no está en vivo')
        except Exception as e:
            pass
            
        
    time.sleep(5)