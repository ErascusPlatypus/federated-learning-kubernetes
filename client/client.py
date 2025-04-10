# client.py
import flwr as fl
from river import anomaly
from river import preprocessing
import numpy as np
import pickle

# Simulated metric stream (replace with real data collection from Prometheus or logs)
def get_data():
    for _ in range(1000):   
        x = np.random.normal(0, 1, 1)[0]
        yield {"metric": x}

# River model
model = preprocessing.MinMaxScaler() | anomaly.HalfSpaceTrees(seed=42, n_trees=10)

# Flower Client
class RiverClient(fl.client.NumPyClient):
    def __init__(self):
        self.model = model
        self.data = list(get_data())

    def get_parameters(self, config):
        return [pickle.dumps(self.model)]

    def fit(self, parameters, config):
        self.model = pickle.loads(parameters[0])
        for x in self.data:
            self.model.learn_one(x)
        return [pickle.dumps(self.model)], len(self.data), {}

    def evaluate(self, parameters, config):
        self.model = pickle.loads(parameters[0])
        # Here, you'd run actual anomaly detection logic
        return 0.0, len(self.data), {"anomalies_detected": 0}

fl.client.start_numpy_client(server_address="flower-server:8080", client=RiverClient())
