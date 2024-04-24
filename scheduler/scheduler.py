#! /usr/bin/python3
import qbittorrentapi
import os
import re
from apscheduler.schedulers.blocking import BlockingScheduler
from sql import Sql
from datetime import date, datetime

def clean_str(string):
    normal_string = re.sub(r"[^A-Z0-9_[\]\.(){} -]", "_",string,0,re.IGNORECASE)
    return normal_string

def log(string):
    time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f"[{time}] {string}", flush=True)

def fetch_and_store():
    log("Fetching data ...")
    db  = Sql(os.getenv('MYSQL_DATABASE'))
    day = date.today().strftime('%d/%m/%Y')

    torrents = qbt_client.torrents_info()
    for torrent in torrents:
        req = f"""REPLACE INTO torrent_data (name, uploaded, downloaded, ratio, size, day) VALUES (
            '{clean_str(torrent.name)}', '{torrent.uploaded/(1024*1024)}', '{torrent.downloaded/(1024*1024)}','{round(torrent.ratio*100,3)}%', '{torrent.size}', '{day}' )
        """
        db.insert(req)
    db.close()
    log("Data fetched")


#---------------------------------------------------------------------------------------------
qbt_client = qbittorrentapi.Client(
     host=os.getenv('QB_HOST'),
     port=os.getenv('QB_PORT'),
     username=os.getenv('QB_USER'),
     password=os.getenv('QB_PASS')
  )

try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(f"Cannot login {e}")
    exit(1)

log("Initial fetch...")
fetch_and_store()
log("Initial fetch done")

log("Scheduler started")
scheduler = BlockingScheduler()
scheduler.add_job(fetch_and_store, 'interval', hours=1)
# scheduler.add_job(fetch_and_store, 'interval', minutes=1)

try:
    scheduler.start()
except KeyboardInterrupt:
    pass
