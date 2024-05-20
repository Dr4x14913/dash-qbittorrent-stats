from sql import Sql
import pandas as pd

def my_float(number):
    try:
        return float(number)
    except Exception:
        return 0

def get_latest_date():
    db = Sql("website")
    res = db.select("SELECT day FROM torrents GROUP BY day ORDER BY STR_TO_DATE(day, '%d/%m/%Y') DESC LIMIT 1")
    db.close()
    return res[0][0]

def get_second_latest_date():
    db = Sql("website")
    res = db.select("SELECT day FROM torrents GROUP BY day ORDER BY STR_TO_DATE(day, '%d/%m/%Y') DESC LIMIT 2")
    return res[1][0]

def get_torrent_list():
    cols          = ['name', 'ratio', 'downloaded', 'uploaded']
    db            = Sql("website")
    latest        = db.select_to_df(f"SELECT  {', '.join(cols)} FROM torrents WHERE day='{get_latest_date()}'", cols)
    second_latest = db.select_to_df(f"SELECT  {', '.join(cols)} FROM torrents WHERE day='{get_second_latest_date()}'", cols)
    db.close()
    # print(latest.to_dict('index'), flush=True)
    # print(second_latest.to_dict('index'), flush=True)
    main_list = []
    print(len(latest), len(second_latest), flush=True)
    for torrent in latest.to_dict('index').values():
        print(torrent, flush=True)
        name         = torrent['name']
        ratio        = torrent['ratio']
        downloaded_l = my_float(torrent['downloaded'])
        uploaded_l   = my_float(torrent['uploaded'])

        sl = second_latest.loc[second_latest['name'] == name].to_dict('list')
        if len(sl['name']) == 0:
            sl['downloaded'] = [0]
            sl['uploaded']   = [0]
        downloaded_sl = my_float(sl['downloaded'][0])
        uploaded_sl   = my_float(sl['uploaded'][0])

        delta_up   = my_round(uploaded_l - uploaded_sl)
        delta_down = my_round(downloaded_l - downloaded_sl)
        up         = my_round(uploaded_l)
        down       = my_round(downloaded_l)

        main_list.append([name, ratio, down, up, delta_up, delta_down])

    return pd.DataFrame(main_list, columns=cols + ["delta up", "delta down"])

def my_round(fl):
    try:
        fl = float(fl)
    except Exception:
        fl = 0.0
    units = ["Mib","Gib","Tib"]
    i = 0
    while True:
        if (fl / 1024) >= 1:
            fl /= 1024
            i += 1
        else:
            return str(round(fl,2)) + " " + units[i]
