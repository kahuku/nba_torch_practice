from nba_api.stats.static import players
import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import argparse

from models import NeuralNetwork
from functions import *
from datasets import GamelogDataset

BATCH_SIZE = 64

parser = argparse.ArgumentParser("python3 main.py")
parser.add_argument('-l', '--load', default=True)

if __name__ == "__main__":
    args = parser.parse_args()

    player_dict = players.get_active_players()

    players = get_player_names(player_dict)
    print("Got players")

    player_ids = get_player_ids(players, player_dict)
    print("Got player IDs")
    #print(player_ids)

    dataset = GamelogDataset(players, 480)
    dataloader = DataLoader(dataset=dataset, batch_size=BATCH_SIZE, shuffle=True)

    model = NeuralNetwork()
    if args.load:
        model.load_state_dict(torch.load("model.pth"))

    lr = 0.001
    #momentum = 1
    loss_fn = nn.L1Loss()
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)

    for i in range(100):
        train(dataloader, model, loss_fn, optimizer)

    torch.save(model.state_dict(), "model.pth")
    print("Finished")
