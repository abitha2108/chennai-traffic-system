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

print("🚀 FINAL RL Simulation started...")

step = 0
file_name = "traffic_rl.csv"

# ---------------- Q-TABLE ----------------
Q = {}
actions = [0, 1, 2]  # short, medium, long

alpha = 0.1
gamma = 0.9
epsilon = 0.1

# ---------------- CSV HEADER ----------------
with open(file_name, "w") as f:
    f.write("step,signal,queue,action,throughput,delay\n")

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

# ---------------- GUI SETUP ----------------
def setup_gui():
    try:
        view = "View #0"
        traci.gui.setSchema(view, "real world")
        xmin, ymin, xmax, ymax = traci.simulation.getNetBoundary()
        traci.gui.setBoundary(view, xmin, ymin, xmax, ymax)
        traci.gui.setZoom(view, 1200)
    except:
        pass

# ---------------- MAIN LOOP ----------------
while step < 5000:

    traci.simulationStep()
    setup_gui()

    # ✅ Throughput
    throughput = traci.simulation.getArrivedNumber()

    # ✅ Delay (waiting time)
    vehicles = traci.vehicle.getIDList()
    total_delay = 0
    for v in vehicles:
        total_delay += traci.vehicle.getWaitingTime(v)

    tls_list = traci.trafficlight.getIDList()

    # ✅ Corridor-level queue
    total_network_queue = sum(
        traci.lane.getLastStepHaltingNumber(l)
        for tl2 in tls_list
        for l in traci.trafficlight.getControlledLanes(tl2)
    )

    for tl in tls_list:

        lanes = traci.trafficlight.getControlledLanes(tl)

        total_queue = 0
        for lane in lanes:
            total_queue += traci.lane.getLastStepHaltingNumber(lane)

        # ✅ FAILURE SIMULATION
        if random.random() < 0.1:
            total_queue *= 0.5

        # ✅ INCIDENT (NEW)
        incident = 1 if random.random() < 0.05 else 0

        # ✅ STATE (FULL)
        current_phase = traci.trafficlight.getPhase(tl)
        time_of_day = step % 1440

        state = (
            int(total_queue / 5),
            current_phase,
            int(time_of_day / 60),
            incident
        )

        # ✅ ACTION
        action = choose_action(state)

        # 🚑 EMERGENCY PRIORITY
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

        # 🌧️ WEATHER
        weather = "clear"
        if weather == "rain":
            duration += 10

        # ✅ CONSTRAINT
        duration = max(15, min(duration, 60))

        traci.trafficlight.setPhaseDuration(tl, duration)

        # ✅ REWARD (FULL POWER 🔥)
        reward = (
            -total_network_queue              # corridor optimization
            + (throughput * 2)               # throughput
            - abs(total_queue - 10)          # fairness
            - (total_delay * 0.01)           # delay penalty
        )

        next_state = state

        update_q(state, action, reward, next_state)

        print(f"Step:{step} | TL:{tl} | Queue:{total_queue} | Dur:{duration} | Th:{throughput} | Delay:{total_delay}")

        # ✅ SAVE CSV
        with open(file_name, "a") as f:
            f.write(f"{step},{tl},{total_queue},{action},{throughput},{total_delay}\n")

    step += 1

traci.close()
print("✅ FINAL RL Simulation completed.")