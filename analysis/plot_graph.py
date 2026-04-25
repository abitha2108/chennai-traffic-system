import pandas as pd
import matplotlib.pyplot as plt

# Load CSV (IMPORTANT PATH)
df = pd.read_csv("../sumo/traffic_log.csv")

# Average queue per step
avg_queue = df.groupby("step")["queue"].mean()

# Plot
plt.figure()
plt.plot(avg_queue)
plt.xlabel("Time Step")
plt.ylabel("Average Queue Length")
plt.title("Traffic Congestion Over Time")
plt.grid()
plt.show()