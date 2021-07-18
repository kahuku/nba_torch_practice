from nba_api.stats.static import players
import argparse
import numpy as np
from nba_api.stats.endpoints import playergamelog
import time
from pathlib import Path
import csv

def get_player_gamelogs(ids):
    gamelogs = []
    i = 0
    while i < len(ids):
        log = playergamelog.PlayerGameLog(player_id=ids[i], season='2019')
        log = log.get_data_frames()
        log = log[0]
        log = log.drop(["Game_ID", "Player_ID", "SEASON_ID", "GAME_DATE", "MATCHUP", "WL", "VIDEO_AVAILABLE"], axis=1)
        log = log.to_numpy(dtype='float32')
        log = normalize_gamelog(log)
        gamelogs.append(log)
        #print("Got gamelog", ids[i])
        filepath = Path("./gamelog_csvs/" + str(ids[i]) + ".csv")
        if (not filepath.exists()) or ('201162' in str(filepath)):
            write_log(ids[i], log)
        i += 1
        time.sleep(2)
    return gamelogs

def write_log(id, gamelog):
    file_name = "./gamelog_csvs/" + str(id) + '.csv'
    open_file = open(file_name, 'w')
    writer = csv.writer(open_file)

    log = gamelog
    counter = 0
    for row in log:
        writer.writerow(row)
        counter += 1

    open_file.close()
    print("Wrote log", id)

def normalize_gamelog(gamelog):
    averages = []
    log = gamelog
    for k in range(20):
        sum = 0
        i = 0
        while i < len(log):
            sum += log[i][k]
            i += 1
        k += 0
        if i != 0:
            averages.append(sum / i)
        else:
            averages.append(0)
    makeup_games = 82 - i
    for game in range(makeup_games):
        log = np.insert(log, len(log), averages, axis=0)

def get_player_ids(player_names, player_dict):
    pids = []
    i = 0
    while i < len(player_names):
        pids.append([player for player in player_dict if player['full_name'] == player_names[i]][0]['id'])
        i += 1
    return pids

def get_player_names(player_dict):
    players = []
    i = 0
    player_list = list(player_dict)
    while i < len(player_dict):
        players.append(player_list[i]['full_name'])
        i += 1
    return players

def download_player_gamelogs(player_ids):
    scores = get_player_scores(player_ids)
    i = 0
    while i < len(player_ids):
        print(scores[i], player_ids[i])
        filename = "./scores/" + str(player_ids[i]) + ".csv"
        open_file = open(filename, 'w')
        writer = csv.writer(open_file)
        writer.writerow([scores[i]])
        open_file.close()
        i += 1

def get_player_scores(ids):
    print("In get scores")
    gamelogs = []
    scores = []
    i = 0
    while i < len(ids):
        log = playergamelog.PlayerGameLog(player_id=ids[i], season='2020').get_data_frames()
        print("Got log", ids[i])
        log = log[0]
        log = log.drop(["Game_ID", "Player_ID", "SEASON_ID", "GAME_DATE", "MATCHUP", "WL", "VIDEO_AVAILABLE"], axis=1)
        log = log.to_numpy(dtype='float32')
        gamelogs.append(log)
        time.sleep(2)
        i += 1
    i = 0
    while i < len(ids):
        log = gamelogs[i]
        sum = 0
        j = 0
        while j < len(log):
            sum += log[j][18]
            j += 1
        if j != 0:
            scores.append(sum / j)
        else:
            scores.append(0)
        i += 1
    print()
    return scores

parser = argparse.ArgumentParser("python3 main.py")
parser.add_argument("-d", "--download", default=False, help="Download the player gamelogs")
parser.add_argument("-s", "--download_scores", default=False, help="Download the player scores")

args = parser.parse_args()

player_dict = players.get_active_players()

players = get_player_names(player_dict)
print("Got players")

player_ids = get_player_ids(players, player_dict)
print("Got player IDs")

#player_ids = ['2544', '201162']

if args.download:
    print("Downloading gamelogs")
    get_player_gamelogs(player_ids)

if args.download_scores:
    print("Downloading scores")
    download_player_gamelogs(player_ids)