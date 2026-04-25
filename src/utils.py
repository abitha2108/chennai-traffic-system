import pandas as pd
import numpy as np

def load_data():
    traffic = pd.read_csv("data/traffic.csv")
    weather = pd.read_csv("data/weather.csv")
    accident = pd.read_csv("data/accident.csv")
    return traffic, weather, accident

def get_state():
    traffic, weather, accident = load_data()

    queue = traffic["vehicle_count"].values
    rain = weather["impact"].values[0]
    
    return queue, rain

def simple_ai_signal(queue):
    return int(np.argmax(queue))