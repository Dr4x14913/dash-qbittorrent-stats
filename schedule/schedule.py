#! /usr/bin/python3
import qbittorrentapi
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from sql import Sql
from datetime import date

def fetch_and_store():
    print("Fetching data ...", flush=True)
    db  = Sql(os.getenv('MYSQL_DATABASE'))
    day = date.today().strftime('%d/%m/%Y')

    torrents = qbt_client.torrents_info()
    for torrent in torrents:
        req = f"""REPLACE INTO torrent_data (name, uploaded, ratio, size, day) VALUES (
            '{torrent.name}', '{torrent.uploaded/(1024*1024)}', '{round(torrent.ratio*100,3)}%', '{torrent.size}', '{day}' )
        """
        db.insert(req)
    db.close()
    print("Data fetched", flush=True)


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
    print(e)

print("Scheduler started", flush=True)
scheduler = BlockingScheduler()
scheduler.add_job(fetch_and_store, 'interval', seconds=10)
# scheduler.add_job(fetch_and_store, 'interval', minutes=1)

try:
    scheduler.start()
except KeyboardInterrupt:
    pass

