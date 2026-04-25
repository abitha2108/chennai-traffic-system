import numpy as np
import random

class TrafficEnv:
    def __init__(self):
        self.state = np.zeros(4)  # queue lengths

    def reset(self):
        self.state = np.random.randint(0, 20, size=4)
        return self.state

    def step(self, action):
        # action: which lane gets green
        reward = -sum(self.state)

        # reduce selected lane
        self.state[action] = max(0, self.state[action] - random.randint(5,10))

        # increase others
        for i in range(4):
            if i != action:
                self.state[i] += random.randint(1,5)

        return self.state, reward