from opacus import PrivacyEngine

class PrivacyManager:
    def __init__(self, model, epsilon=1.0):
        self.engine = PrivacyEngine()
        self.model, self.optimizer, _ = self.engine.make_private(
            module=model,
            optimizer=optimizer,
            max_grad_norm=1.0,
            noise_multiplier=1.1
        )