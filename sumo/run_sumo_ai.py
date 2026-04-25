import traci
import os
import sys

# ---------------- SUMO PATH ----------------
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare SUMO_HOME")

# ---------------- START SUMO ----------------
sumo_cmd = ["sumo-gui", "-c", "config.sumocfg"]

traci.start(sumo_cmd)

print("🚀 Simulation started...")

step = 0

while step < 5000:

    traci.simulationStep()

    # ---------------- FIX 1: CHECK VEHICLES ----------------
    vehicles = traci.vehicle.getIDList()
    print("Vehicles:", len(vehicles))

    # ---------------- FIX 2: FORCE GUI ----------------
    try:
        traci.gui.setZoom("View #0", 800)

        xmin, ymin, xmax, ymax = traci.simulation.getNetBoundary()
        traci.gui.setBoundary("View #0", xmin, ymin, xmax, ymax)

        traci.gui.setSchema("View #0", "real world")

    except:
        pass

    # ---------------- TRAFFIC LIGHT LOGIC ----------------
    tls_list = traci.trafficlight.getIDList()

    for tl in tls_list:

        lanes = traci.trafficlight.getControlledLanes(tl)

        total_queue = 0
        for lane in lanes:
            total_queue += traci.lane.getLastStepHaltingNumber(lane)

        # SIMPLE AI LOGIC
        if total_queue > 20:
            duration = 40
        elif total_queue > 10:
            duration = 30
        else:
            duration = 15

        traci.trafficlight.setPhaseDuration(tl, duration)

        print(f"Step: {step} | Signal: {tl} | Queue: {total_queue}")

    step += 1

traci.close()
print("✅ Simulation ended.")