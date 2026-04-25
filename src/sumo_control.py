import traci
import time

sumo_cmd = ["sumo-gui", "-c", "sumo/config.sumocfg"]
traci.start(sumo_cmd)

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    # get queue length
    vehicles = traci.vehicle.getIDList()
    queue = len(vehicles)

    print("Queue:", queue)

    # simple AI logic (baseline)
    if queue > 20:
        traci.trafficlight.setPhaseDuration("junction0", 30)
    else:
        traci.trafficlight.setPhaseDuration("junction0", 10)

    time.sleep(0.1)

traci.close()