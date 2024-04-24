from sql import Sql
import pandas as pd

def get_latest_date():
    db = Sql("website")
    res = db.select("SELECT day FROM torrent_data GROUP BY day ORDER BY STR_TO_DATE(day, '%d/%m/%Y') DESC LIMIT 1")
    return res[0][0]

def get_second_latest_date():
    db = Sql("website")
    res = db.select("SELECT day FROM torrent_data GROUP BY day ORDER BY STR_TO_DATE(day, '%d/%m/%Y') DESC LIMIT 2")
    return res[1][0]

def get_torrent_list():
    cols          = ['name', 'ratio', 'downloaded', 'uploaded']
    db            = Sql("website")
    latest        = db.select_to_df(f"SELECT  {', '.join(cols)} FROM torrent_data WHERE day='{get_latest_date()}'", cols)
    second_latest = db.select_to_df(f"SELECT  {', '.join(cols)} FROM torrent_data WHERE day='{get_second_latest_date()}'", cols)
    db.close()
    # print(latest.to_dict('index'), flush=True)
    # print(second_latest.to_dict('index'), flush=True)
    main_list = []

    for torrent in latest.to_dict('index').values():
        name         = torrent['name']
        ratio        = torrent['ratio']
        downloaded_l = float(torrent['downloaded']) if torrent['downloaded'] is not None else 0
        uploaded_l   = float(torrent['uploaded']) if torrent['uploaded'] is not None else 0

        sl = second_latest.loc[second_latest['name'] == name].to_dict('list')
        try:
            downloaded_sl = float(sl['downloaded'][0])
        except Exception:
            downloaded_sl = 0
        try:
            uploaded_sl   = float(sl['uploaded'][0])
        except Exception:
            uploaded_sl   = 0

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
