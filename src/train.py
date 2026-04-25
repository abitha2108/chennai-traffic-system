from agent import Agent
from environment import TrafficEnv

env = TrafficEnv()
agent = Agent(state_size=4, action_size=4)

episodes = 100

for ep in range(episodes):
    state = env.reset()

    for step in range(50):
        action = agent.act(state)
        next_state, reward = env.step(action)

        agent.train(state, action, reward, next_state)
        state = next_state

    print(f"Episode {ep} completed")