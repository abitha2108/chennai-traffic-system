import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, action_size)
        )

    def forward(self, x):
        return self.fc(x)


class Agent:
    def __init__(self, state_size, action_size):
        self.model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        self.gamma = 0.95

    def act(self, state):
        state = torch.FloatTensor(state)
        q_values = self.model(state)
        return torch.argmax(q_values).item()

    def train(self, state, action, reward, next_state):
        state = torch.FloatTensor(state)
        next_state = torch.FloatTensor(next_state)

        target = reward + self.gamma * torch.max(self.model(next_state))
        output = self.model(state)[action]

        loss = self.criterion(output, target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()