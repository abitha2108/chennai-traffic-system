import pandas as pd

df = pd.read_csv("data/traffic_counts.csv")

with open("sumo/routes.rou.xml", "w") as f:
    f.write("<routes>\n")

    # vehicle type
    f.write('<vType id="car" accel="1.0" decel="4.5" length="5" maxSpeed="25"/>\n')

    for i, row in df.iterrows():
        f.write(f'''
        <vehicle id="veh{i}" type="car" depart="{i}">
            <route edges="A1B1 B1A1"/>
        </vehicle>
        ''')

    f.write("</routes>")