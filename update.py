from telethon.sync import TelegramClient
from pytz import timezone
from datetime import timedelta
from datetime import date
import pytz
import pandas as pd
import streamlit as st
import re

import configparser
config = configparser.ConfigParser()
config.read("telethon.config")

api_id = config["telethon_credentials"]["api_id"]
api_hash = config["telethon_credentials"]["api_hash"]
username = config['telethon_credentials']['username']

chats = ['lootbot','dealsworldchannel', 'TrickXpert', 'dealspoint', 'FRCP_Official', 'deals_battle_extra', 'deals_battle', 'kooltech007', 'Offer_point_Deals']
dates = [date.today(),  date.today()-timedelta(days = 1)]
client =  TelegramClient(username, api_id, api_hash)


df = pd.DataFrame()

def remove_stars(x):
    x = ' '.join(str(x).split('\n'))
    x = ''.join(x.split('*'))
    return x

for chat in chats:
    for crr_date in dates:
        with TelegramClient(username, api_id, api_hash) as client:
            # datetime.datetime.utcnow().date()
            for message in client.iter_messages(chat, offset_date=crr_date, reverse=True):
                # print(message)
                # pattern = r'[^\w\s]'
                # try:
                #     text = re.sub(pattern, '', str(message.text))
                # except:
                text = remove_stars(message.text)
                try:
                    link = re.search("(?P<url>https?://[^\s]+)", text).group("url")
                except:
                    link = None


                data = { "group" : chat, 
                        "sender" : message.sender_id, 
                        "link" : link, 
                        "text" : text, 
                        "date" : message.date}

                temp_df = pd.DataFrame(data, index=[1])
                df = pd.concat([temp_df, df], ignore_index=True ) 

df['date'] = df['date'].dt.tz_convert(pytz.timezone('Asia/Kolkata'))
# df['text'] = df['text'].apply(lambda x: re.sub(pattern, '', x))

df.to_csv("data_{}.csv".format(date.today()), index=False)

