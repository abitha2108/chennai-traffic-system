import pandas as pd
import matplotlib.pyplot as plt

# Load files
normal = pd.read_csv("../sumo/traffic_normal.csv")
ai = pd.read_csv("../sumo/traffic_ai.csv")
rl = pd.read_csv("../sumo/traffic_rl.csv")

# Average queue
normal_avg = normal.groupby("step")["queue"].mean()
ai_avg = ai.groupby("step")["queue"].mean()
rl_avg = rl.groupby("step")["queue"].mean()

# Plot
plt.figure()

plt.plot(normal_avg, label="Normal", linestyle="--")
plt.plot(ai_avg, label="AI", linewidth=2)
plt.plot(rl_avg, label="RL", linewidth=3)

plt.xlabel("Time Step")
plt.ylabel("Average Queue")
plt.title("Traffic Optimization: Normal vs AI vs RL")

plt.legend()
plt.grid()

plt.show()

# Throughput comparison
print("Normal Throughput:", normal["queue"].count())
print("AI Throughput:", ai["queue"].count())
print("RL Throughput:", rl["queue"].count())

print("Normal Avg Queue:", normal_avg.mean())
print("AI Avg Queue:", ai_avg.mean())
print("RL Avg Queue:", rl_avg.mean())