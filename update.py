from telethon.sync import TelegramClient
from pytz import timezone
from datetime import timedelta
from datetime import date
import pytz
import pandas as pd
import re
from asyncio import run

import configparser
config = configparser.ConfigParser()
config.read("telethon.config")

api_id = config["telethon_credentials"]["api_id"]
api_hash = config["telethon_credentials"]["api_hash"]
username = config['telethon_credentials']['username']

chats = ['lootbot','dealsworldchannel', 'TrickXpert', 'dealspoint', 'FRCP_Official', 'deals_battle_extra', 'deals_battle', 'kooltech007']
dates = [date.today(),  date.today()-timedelta(days = 1)]


df = pd.DataFrame()

def remove_stars(x):
    x = ' '.join(str(x).split('\n'))
    x = ''.join(x.split('*'))
    return x

for chat in chats:
    for crr_date in dates:
        with TelegramClient(username, api_id, api_hash) as client:
            for message in client.iter_messages(chat, offset_date=crr_date, reverse=True):
                text = remove_stars(message.text)
                try:
                    link = re.search("(?P<url>https?://[^\s]+)", text).group("url")
                    if 'youtu.be' not in link and 't.me' not in link and 'bit.ly' not in link:
                        data = {"link" : link, 
                                "description" : text, 
                                "date" : message.date}
                        temp_df = pd.DataFrame(data, index=[1])
                        df = pd.concat([temp_df, df], ignore_index=True ) 
                except:
                    pass
def remove_http(text):
    text = ' '.join(str(text).split('\n'))
    http = "https?://\S+|www\.\S+" 
    pattern = r"({})".format(http) # creating pattern
    return re.sub(pattern, "", text)

def remove_stars(x):
    x = ' '.join(str(x).split('\n'))
    x = ''.join(x.split('*'))
    x = ''.join(x.split(')'))
    x = ''.join(x.split('('))
    return x

df.description = df.description.apply(lambda x : remove_http(x))
df.link = df.link.apply(lambda x : remove_stars(x))

df.to_csv("raw_data.csv".format(date.today()), index=False)