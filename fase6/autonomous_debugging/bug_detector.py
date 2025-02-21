import re
import logging
from functools import lru_cache

class BugDetector:
    def __init__(self):
        self.logger = logging.getLogger("BugDetector")
    
    @lru_cache(maxsize=1000)
    def detect(self, error_log: str) -> dict:
        """Clasifica errores comunes"""
        patterns = {
            "NullPointer": r"null pointer",
            "MemoryLeak": r"memory leak",
            "RaceCondition": r"race condition"
        }
        return {k: bool(re.search(p, error_log)) for k, p in patterns.items()}