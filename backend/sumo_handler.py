import traci

def connect_sumo():
    if not traci.isLoaded():
        traci.connect(port=8830)

def step():
    traci.simulationStep()

def get_vehicle_count():
    edges = traci.edge.getIDList()

    counts = []
    for edge in edges[:4]:
        counts.append(traci.edge.getLastStepVehicleNumber(edge))

    return counts