import unittest
from ai_coder.complexity_analyzer import ComplexityAnalyzer

class TestComplexityAnalysis(unittest.TestCase):
    def setUp(self):
        self.analyzer = ComplexityAnalyzer()
    
    def test_sorting_complexity(self):
        code = """
        def quicksort(arr):
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return quicksort(left) + middle + quicksort(right)
        """
        metrics = self.analyzer.analyze(code)
        self.assertEqual(metrics['time_complexity'], "O(n log n)")
    
    def test_fibonacci_complexity(self):
        code = """
        def fibonacci(n):
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            return a
        """
        metrics = self.analyzer.analyze(code)
        self.assertEqual(metrics['time_complexity'], "O(n)")

if __name__ == '__main__':
    unittest.main()