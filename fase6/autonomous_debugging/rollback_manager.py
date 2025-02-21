import subprocess

class RollbackManager:
    def __init__(self, repo_path: str):
        self.repo = repo_path
    
    def safe_rollback(self, commit_hash: str):
        """Revierte cambios de manera segura"""
        subprocess.run(["git", "checkout", commit_hash], cwd=self.repo, check=True)
        subprocess.run(["docker-compose", "down"], cwd=self.repo, check=True)
        subprocess.run(["docker-compose", "up", "-d"], cwd=self.repo, check=True)