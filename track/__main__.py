from datetime import datetime
from settings import API_ID, API_HASH
from sys import argv, exit
from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline, UserStatusOffline
from time import mktime, sleep


DATETIME_FORMAT = '%Y-%m-%d @ %H:%M:%S'


def utc2localtime(utc):
    pivot = mktime(utc.timetuple())
    offset = datetime.fromtimestamp(pivot) - datetime.utcfromtimestamp(pivot)
    return utc + offset


if len(argv) < 2:
    print(f'usage: {argv[0]} <contact id>')
    exit(1)
contact_id = argv[1]

client = TelegramClient('tracker', API_ID, API_HASH)
client.start()

online = None
last_offline = None
while True:
    contact = client.get_entity(contact_id)
    if isinstance(contact.status, UserStatusOffline):
        if online != False:
            online = False
            print(f'User went offline: {utc2localtime(contact.status.was_online).strftime(DATETIME_FORMAT)}')
        elif last_offline != contact.status.was_online:
            if last_offline is not None:
                print(f'User went online and back offline: {utc2localtime(contact.status.was_online).strftime(DATETIME_FORMAT)}')
            else:
                print(f'User went offline: {utc2localtime(contact.status.was_online).strftime(DATETIME_FORMAT)}')
        last_offline = contact.status.was_online
    elif isinstance(contact.status, UserStatusOnline):
        if online != True:
            online = True
            print(f'User went online: {datetime.now().strftime(DATETIME_FORMAT)}')
    else:
        if online != False:
            online = False
            print(f'User went offline: around {datetime.now().strftime(DATETIME_FORMAT)}')
        last_offline = None
    sleep(15)