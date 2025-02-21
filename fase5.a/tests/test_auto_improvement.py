import unittest
from auto_improvement.self_improvement_engine import SelfImprovementEngine

class TestAutoImprovement(unittest.TestCase):
    def setUp(self):
        self.engine = SelfImprovementEngine(mock_ai)
    
    def test_optimization(self):
        test_code = "def sum(a,b): return a+b"
        optimized = self.engine.optimize_code(test_code)
        self.assertIn("def sum", optimized)
    
    def test_metrics(self):
        metrics = self.engine._analyze_code("print('test')")
        self.assertGreater(metrics['execution_time'], 0)