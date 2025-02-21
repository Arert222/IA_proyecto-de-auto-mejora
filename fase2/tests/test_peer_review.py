import unittest
from ai_coder.peer_review import PeerReviewSystem

class TestPeerReview(unittest.TestCase):
    def setUp(self):
        self.review_system = PeerReviewSystem()
    
    def test_competition_flow(self):
        prompt = "Función Python para invertir una cadena"
        result = self.review_system.code_competition(prompt, rounds=1)
        
        self.assertIn("def", result["code"])
        self.assertGreater(result["score"], 0)
    
    def test_evaluation_consistency(self):
        code = "def suma(a, b): return a + b"
        scores = []
        
        for _ in range(5):
            score = self.review_system._evaluate_solution(
                code, 
                self.review_system.agents[:2],
                "Suma dos números"
            )
            scores.append(score)
        
        avg = sum(scores)/len(scores)
        self.assertTrue(5.0 <= avg <= 9.0)

if __name__ == "__main__":
    unittest.main()