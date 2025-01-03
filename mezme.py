from federated_learning import FederatedLearning
from zk_proofs import ZeroKnowledgeProofs
import numpy as np

class Mezme:
    def __init__(self):
        self.federated_learning = FederatedLearning()
        self.zk_proofs = ZeroKnowledgeProofs()

    def process_data(self, local_data, global_model, use_federated=True, use_zk=False):
        if use_federated:
            # Federated Learning approach
            local_model = self.federated_learning.train_local_model(local_data, global_model)
            # Here, we would typically aggregate results on a central server, but for this example, we'll simulate it:
            global_model = self.federated_learning.aggregate_models([local_model])
            return global_model, None  # No sensitive data is shared

        elif use_zk:
            # Zero-Knowledge Proofs for data verification without revealing data
            proof = self.zk_proofs.generate_proof(local_data)
            # Validate the proof on the server side
            if self.zk_proofs.verify_proof(proof):
                # If proof is valid, we can proceed with computation on encrypted data or with assurances
                return global_model, proof
            else:
                raise ValueError("Invalid zero-knowledge proof")
        
        else:
            raise NotImplementedError("Either federated learning or zero-knowledge proofs must be selected.")

    def predict(self, model, data):
        # Here we use the model to make predictions without accessing the original data directly
        return model.predict(data)

if __name__ == "__main__":
    mezme = Mezme()
    
    # Simulating data from clients
    client_data = np.array([[1, 2], [3, 4], [5, 6]])  # Example data for one client

    # Initial model (in practice, this would be a more complex model)
    global_model = np.mean(client_data, axis=0)  # Simple average model for demonstration
    
    # Federated Learning
    new_model_fed, _ = mezme.process_data(client_data, global_model, use_federated=True, use_zk=False)
    print("Federated Learning Updated Model:", new_model_fed)
    
    # Zero-Knowledge Proofs
    _, proof = mezme.process_data(client_data, global_model, use_federated=False, use_zk=True)
    print("Zero-Knowledge Proof Generated:", proof)
    
    # Use the model for prediction
    prediction = mezme.predict(new_model_fed, client_data)
    print("Prediction with federated learning model:", prediction)
