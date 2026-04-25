import traci
import os
import sys
import random

# ---------------- SUMO PATH ----------------
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare SUMO_HOME")

# ---------------- START SUMO ----------------
sumo_cmd = ["sumo-gui", "-c", "config.sumocfg"]
traci.start(sumo_cmd)

print("🚀 RL Simulation started...")

step = 0
file_name = "traffic_rl.csv"

# ---------------- Q-TABLE ----------------
Q = {}
actions = [0, 1, 2]

alpha = 0.1
gamma = 0.9
epsilon = 0.1

# ---------------- CSV HEADER ----------------
with open(file_name, "w") as f:
    f.write("step,signal,queue,action,throughput\n")

# ---------------- FUNCTIONS ----------------
def get_q(state, action):
    return Q.get((state, action), 0)

def choose_action(state):
    if random.random() < epsilon:
        return random.choice(actions)
    else:
        q_values = [get_q(state, a) for a in actions]
        return actions[q_values.index(max(q_values))]

def update_q(state, action, reward, next_state):
    old_q = get_q(state, action)
    future_q = max([get_q(next_state, a) for a in actions])
    Q[(state, action)] = old_q + alpha * (reward + gamma * future_q - old_q)

# 🔥 GUI SETUP FUNCTION (UPDATED)
def setup_gui():
    try:
        view = "View #0"

        # 🎨 Clean realistic view
        traci.gui.setSchema(view, "real world")

        # 🗺️ Center full map
        xmin, ymin, xmax, ymax = traci.simulation.getNetBoundary()
        traci.gui.setBoundary(view, xmin, ymin, xmax, ymax)

        # 🔍 Zoom control (CHANGE HERE)
        traci.gui.setZoom(view, 1200)   # normal view
        # traci.gui.setZoom(view, 2000) # demo close view

    except:
        pass

# ---------------- MAIN LOOP ----------------
while step < 5000:

    traci.simulationStep()

    # 🔥 GUI FIX EVERY STEP
    setup_gui()

    # ✅ THROUGHPUT
    throughput = traci.simulation.getArrivedNumber()

    tls_list = traci.trafficlight.getIDList()

    for tl in tls_list:

        lanes = traci.trafficlight.getControlledLanes(tl)

        total_queue = 0
        for lane in lanes:
            total_queue += traci.lane.getLastStepHaltingNumber(lane)

        # ✅ FAILURE SIMULATION
        if random.random() < 0.1:
            total_queue *= 0.5

        # ✅ STATE
        current_phase = traci.trafficlight.getPhase(tl)
        time_of_day = step % 1440
        state = (int(total_queue/5), current_phase, int(time_of_day/60))

        # ✅ ACTION
        action = choose_action(state)

        # 🚑 EMERGENCY PRIORITY
        vehicles = traci.vehicle.getIDList()

        if any("ambulance" in v.lower() for v in vehicles):
            duration = 60
        else:
            # 🔥 SMART CONTROL
            if total_queue > 30:
                duration = 60
            elif total_queue > 20:
                duration = 45
            elif total_queue > 10:
                duration = 30
            else:
                duration = 15

        # ✅ CONSTRAINT
        duration = max(15, min(duration, 60))

        traci.trafficlight.setPhaseDuration(tl, duration)

        # ✅ REWARD
        reward = -total_queue + (throughput * 2)

        next_state = state
        update_q(state, action, reward, next_state)

        print(f"Step:{step} | TL:{tl} | Queue:{total_queue} | Duration:{duration} | Throughput:{throughput}")

        # ✅ SAVE CSV
        with open(file_name, "a") as f:
            f.write(f"{step},{tl},{total_queue},{action},{throughput}\n")

    step += 1

traci.close()
print("✅ RL Simulation ended.")