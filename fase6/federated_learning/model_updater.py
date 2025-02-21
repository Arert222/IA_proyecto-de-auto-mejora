import torch

class FederatedUpdater:
    def __init__(self, base_model):
        self.model = base_model
    
    def aggregate_updates(self, client_updates: list):
        """Combina actualizaciones de múltiples clientes"""
        averaged_weights = {}
        for key in client_updates[0].keys():
            averaged_weights[key] = torch.mean(
                torch.stack([update[key] for update in client_updates]), dim=0
            )
        self.model.load_state_dict(averaged_weights)