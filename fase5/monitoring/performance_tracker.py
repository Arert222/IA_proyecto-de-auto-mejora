import time
import psutil
from prometheus_client import start_http_server, Gauge

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'cpu_usage': Gauge('ia_cpu_usage', 'Uso de CPU (%)'),
            'memory_usage': Gauge('ia_memory_usage', 'Uso de memoria (MB)'),
            'code_quality': Gauge('ia_code_quality', 'Puntuación calidad código')
        }
        start_http_server(8000)
    
    def track_performance(self):
        while True:
            self.metrics['cpu_usage'].set(psutil.cpu_percent())
            self.metrics['memory_usage'].set(psutil.virtual_memory().used / 1024**2)
            time.sleep(5)

    def update_code_quality(self, code: str):
        """Analiza calidad usando métricas estáticas"""
        complexity = self.calculate_cyclomatic_complexity(code)
        self.metrics['code_quality'].set(100 - complexity)