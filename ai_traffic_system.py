import os
import traci
import time

SUMO_HOME = "C:/Program Files (x86)/Eclipse/Sumo"
os.environ['SUMO_HOME'] = SUMO_HOME

# -----------------------------
# 1. CREATE ROAD NETWORK
# -----------------------------
os.system("netgenerate --grid --grid.number=3 --tls.guess true --output-file=sumo/map.net.xml")

# -----------------------------
# 2. GENERATE VEHICLES
# -----------------------------
os.system(f'python "{SUMO_HOME}/tools/randomTrips.py" -n sumo/map.net.xml -r sumo/routes.rou.xml -e 1000')

# -----------------------------
# 3. START SUMO
# -----------------------------
traci.start(["sumo-gui", "-c", "sumo/config.sumocfg"])

print("🚦 Simulation Started")

# -----------------------------
# 4. AI SIGNAL CONTROL
# -----------------------------
def get_queue(junction_id):
    lanes = traci.trafficlight.getControlledLanes(junction_id)
    return sum(traci.lane.getLastStepVehicleNumber(l) for l in lanes)

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    tls_ids = traci.trafficlight.getIDList()

    for tls in tls_ids:
        queue = get_queue(tls)

        if queue > 20:
            traci.trafficlight.setPhase(tls, 0)  # green
        else:
            traci.trafficlight.setPhase(tls, 1)  # red

    time.sleep(0.1)

traci.close()
print("Simulation Ended")