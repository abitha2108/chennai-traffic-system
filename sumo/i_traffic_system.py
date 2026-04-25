import traci
import os
import sys

# SUMO PATH
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare SUMO_HOME")

# SUMO command
sumo_cmd = ["sumo-gui", "-c", "config.sumocfg"]

# Start SUMO
traci.start(sumo_cmd)

print("Simulation started...")

step = 0
 #file_name = "traffic_ai.csv"
file_name = "traffic_normal.csv"

# CREATE CSV FILE (HEADER)
with open(file_name, "w") as f:
    f.write("step,signal,queue\n")

while step < 5000:

    traci.simulationStep()

    # GUI CONTROL (SAFE)
    try:
        traci.gui.setSchema("View #0", "realistic")
        xmin, ymin, xmax, ymax = traci.simulation.getNetBoundary()
        traci.gui.setBoundary("View #0", xmin, ymin, xmax, ymax)
    except:
        pass

    # GET SIGNALS
    tls_list = traci.trafficlight.getIDList()

    for tl in tls_list:

        lanes = traci.trafficlight.getControlledLanes(tl)

        total_queue = 0
        for lane in lanes:
            total_queue += traci.lane.getLastStepHaltingNumber(lane)

        # WEATHER CONDITION
        weather = "clear"

        if weather == "rain":
            extra_time = 10
        else:
            extra_time = 0

        # AI DECISION
        if total_queue > 20:
            duration = 40 + extra_time
        elif total_queue > 10:
            duration = 30 + extra_time
        else:
            duration = 15 + extra_time

        traci.trafficlight.setPhaseDuration(tl, duration)

        # PRINT OUTPUT
        print(f"Step: {step} | Signal: {tl} | Queue: {total_queue} | Duration: {duration}")

        # WRITE TO CSV
        with open(file_name, "a") as f:
            f.write(f"{step},{tl},{total_queue}\n")

    step += 1

traci.close()
print("Simulation ended.")