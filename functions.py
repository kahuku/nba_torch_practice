from nba_api.stats.endpoints import playergamelog
import numpy as np
import csv
import torch
import time
from pathlib import Path

def get_player_ids(player_names, player_dict):
    pids = []
    i = 0
    while i < len(player_names):
        pids.append([player for player in player_dict if player['full_name'] == player_names[i]][0]['id'])
        i += 1
    return pids

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

def write_logs(ids, gamelogs):
    i = 0
    while i < len(ids):
        write_log(ids[i], gamelogs[i])

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
    return log

def get_player_scores(ids):
    gamelogs = []
    scores = []
    i = 0
    while i < len(ids):
        log = playergamelog.PlayerGameLog(player_id=ids[i], season='2020').get_data_frames()
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
        scores.append(sum / j)
        #print(ids[i], ":", scores[i], sum, j)
        print(ids[i], ":", scores[i])
        i += 1
    print()
    return scores

def get_player_names(player_dict):
    players = []
    i = 0
    player_list = list(player_dict)
    while i < len(player_dict):
        players.append(player_list[i]['full_name'])
        i += 1
    return players

def train(dataloader, model, loss_fn, optimizer):
    #print("Entered train")
    model.train()
    batch_num = 0
    losses = []
    for (x, y) in dataloader:
        y = y.to(torch.float32).unsqueeze(1)
        outputs = model(x)
        #print(outputs, y)
        loss = loss_fn(outputs, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss = loss.item()
        #print(f"Loss: {loss}, batch_num: {batch_num}")
        losses.append(loss)
        batch_num += 1

    total_loss = 0
    i = 0
    while i < len(losses):
        total_loss += losses[i]
        i += 1
    total_loss /= len(losses)
    print("Loss:", total_loss)

def download_player_scores(player_ids):
    scores = get_player_scores(player_ids)
    print(player_ids[0], scores[0])