from torch.utils.data import Dataset
import torch
import os
import csv

class GamelogDataset(Dataset):
    def __init__(self, players,  num_players):
        self.players = players

        files_list = os.listdir("gamelog_csvs")
        files_list = files_list[:num_players]
        all_tensors = torch.empty(1, 82, 20)
        all_tensors = torch.cat([all_tensors[0:0], all_tensors[1:]])
        ids = []
        for f in files_list:
            csv_file = "./gamelog_csvs/" + f
            open_file = open(csv_file)
            reader = csv.reader(open_file)
            log = self.read_log(reader).unsqueeze(0)
            if log.size()[1] == 82:
                all_tensors = torch.cat((all_tensors, log), 0)
                player_id = int(f.split('.')[0])
                ids.append(player_id)
        self.player_gamelogs = all_tensors

        scores = []
        for player_id in ids:
            file = "./scores/" + str(player_id) + ".csv"
            open_file = open(file)
            reader = csv.reader(open_file)
            for line in reader:
                for entry in line:
                    scores.append(float(entry))
        self.player_scores = scores
        # print(self.player_scores)
        # print(len(self.player_scores))

        self.dict = {self.player_gamelogs[i]: self.player_scores[i] for i in range(len(self.player_gamelogs))}
        # for thing in self.dict:
            # print(thing, self.dict[thing])
            # print()

    def __len__(self):
        return len(self.dict)

    def __getitem__(self, item):
        self.key = list(self.dict)[item]
        self.value = self.dict[self.key]
        return self.key, self.value

    def read_log(self, reader):
        counter = 0
        all_tensors = torch.empty((1, 20))
        all_tensors = torch.cat([all_tensors[0:0], all_tensors[1:]])
        for line in reader:
            tensor_line = []
            for entry in line:
                entry = torch.tensor(float(entry))
                tensor_line.append(entry)
            tensor_line = torch.tensor(tensor_line).unsqueeze(0)
            all_tensors = torch.cat((all_tensors, tensor_line), 0)
            counter += 1
        return all_tensors
