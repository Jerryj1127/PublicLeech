#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import ast 
from random import randint
from os import path, remove
from csv import reader
from re import search 
from requests import get
from zipfile import ZipFile

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import pyrogram


from tobrot import (
    AUTH_CHANNEL
)



url = 'https://webmaster-tools.xvideos.com/xvideos.com-export-week.csv.zip'

def retrive_from_site(url):
    file_name = "xvid.zip"
    
    buffer = get(url, allow_redirects=True)
    open(file_name, 'wb').write(buffer.content)

    with ZipFile(file_name, 'r') as zip:
        zip.extractall()

    remove(file_name)
  

def convert_to_dictionary():
    #checks wrther the file exsts and retrive zip file from site and extracts it
    file_name = 'xvideos.com-export-week.csv'
    if not path.isfile(file_name):
        retrive_from_site(url)
    i=0
    with open(file_name,'r', encoding='utf-8') as f:
        value = reader(f)
        with open('links.txt', 'w') as fl:
            fl.write('{')
            for val in value:
                link = search('^[A-Za-z:\/.0-9_-]*', val[0]).group()
                i+=1
                #Use \n if you want multiline  
                fl.write(str(i) + ':\'' + link +'\', ')     
                #appends to a text file as a dictionary
            fl.write('}')
    remove(file_name)


def fetch():

    if not (path.isfile('links.txt')):
        convert_to_dictionary()

    with open('links.txt', 'r', encoding='utf-8') as f:
        dic= f.read()
    dictionary = ast.literal_eval(dic)
    vid = dictionary[randint(0,63614)]
    return(vid)


def fetch_refresh():
    convert_to_dictionary()
    return(fetch())
    




async def new_join_f(client, message):
    chat_type = message.chat.type
    if chat_type != "private":
        await message.reply_text(f"Current CHAT ID: <code>{message.chat.id}</code>")
        # leave chat
        await client.leave_chat(
            chat_id=message.chat.id,
            delete=True
        )
    # delete all other messages, except for AUTH_CHANNEL
    await message.delete(revoke=True)


async def help_message_f(client, message):
    # await message.reply_text("no one gonna help you 🤣🤣🤣🤣", quote=True)
    channel_id = str(AUTH_CHANNEL)[4:]
    message_id = 99
    # display the /help message
    await message.reply_text(
        f"please read the <a href='https://t.me/c/{channel_id}/{message_id}'>Pinned Message</a>",
        quote=True
    )


async def rename_message_f(client, message):
    inline_keyboard = []
    inline_keyboard.append([
        pyrogram.InlineKeyboardButton(
            text="download?",
            await message.reply_text("/ytdl@ieat1337bot", quote=True)
        )
    ])
    reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)
    await message.reply_text(
        "{}".format(fetch()),
        quote=True,
        reply_markup=reply_markup
    )
