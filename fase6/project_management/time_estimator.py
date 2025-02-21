from datetime import timedelta

class TimeEstimator:
    def estimate(self, codebase: str) -> timedelta:
        """Estima tiempo basado en métricas de código"""
        complexity = self._calculate_complexity(codebase)
        loc = len(codebase.splitlines())
        return timedelta(hours=loc * 0.1 + complexity * 0.5)