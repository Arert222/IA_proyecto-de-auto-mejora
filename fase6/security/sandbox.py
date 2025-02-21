import docker

class CodeSandbox:
    def __init__(self):
        self.client = docker.from_env()
    
    def run_safely(self, code: str):
        """Ejecuta código en contenedor aislado"""
        container = self.client.containers.run(
            "python:3.9-slim",
            command=f"python -c '{code}'",
            mem_limit="100m",
            network_disabled=True,
            remove=True
        )
        return container.logs()