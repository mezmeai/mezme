import numpy as np

class FederatedLearning:
    def train_local_model(self, local_data, global_model):
        # Simulate local training by adjusting the model with local data
        local_update = np.mean(local_data, axis=0)
        return global_model + 0.1 * (local_update - global_model)  # Simple update rule

    def aggregate_models(self, models):
        # Aggregate models from all clients (here just one for simplicity)
        return np.mean(models, axis=0)
